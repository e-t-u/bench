const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

const argv = process.argv.slice(2);
if (argv.length < 3) {
  console.error('Usage: node export_map.js <input_html> <output_file> <format>');
  process.exit(1);
}

const inputHtml = argv[0];
const outputFile = argv[1];
const format = argv[2].toLowerCase();

(async () => {
  let browser;
  try {
    browser = await puppeteer.launch({
      headless: true,
      args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    const page = await browser.newPage();
    
    // Set viewport to a square 1200x1200px
    await page.setViewport({ width: 1200, height: 1200 });
    
    const fileUrl = inputHtml.startsWith('http') ? inputHtml : `file://${path.resolve(inputHtml)}`;
    console.log(`Loading map: ${fileUrl}`);
    
    // Wait for network to be idle so tiles and external resources load
    await page.goto(fileUrl, { waitUntil: 'networkidle0', timeout: 60000 });
    
    // Extra wait to guarantee Leaflet rendering is complete
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    if (format === 'pdf') {
      console.log(`Generating PDF: ${outputFile}`);
      await page.pdf({
        path: outputFile,
        printBackground: true,
        width: '1200px',
        height: '1200px',
        margin: { top: '0px', right: '0px', bottom: '0px', left: '0px' }
      });
      console.log('PDF export completed successfully.');
    } else if (format === 'svg') {
      console.log(`Generating SVG: ${outputFile}`);
      // Find the SVG overlays element
      const svgContent = await page.evaluate(() => {
        const svgEl = document.querySelector('.leaflet-overlay-pane svg');
        if (svgEl) {
          // Add XML namespace attributes if missing
          if (!svgEl.getAttribute('xmlns')) {
            svgEl.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
          }
          return svgEl.outerHTML;
        }
        // Fallback to any SVG
        const fallbackSvg = document.querySelector('svg');
        return fallbackSvg ? fallbackSvg.outerHTML : null;
      });
      
      if (!svgContent) {
        console.error('Error: Leaflet SVG overlay pane not found.');
        process.exit(1);
      }
      
      fs.writeFileSync(outputFile, svgContent);
      console.log('SVG export completed successfully.');
    } else {
      console.error(`Error: Unsupported format '${format}'`);
      process.exit(1);
    }
  } catch (err) {
    console.error('Export failed:', err);
    process.exit(1);
  } finally {
    if (browser) {
      await browser.close();
    }
  }
})();
