
(async () => {
  function extractData() {
    const products = [];
    const items = document.querySelectorAll('.ant-list-item');
    
    items.forEach(item => {
      const titleLink = item.querySelector('a[href*="/products/detail/"]');
      if (!titleLink) return;
      
      const title = titleLink.innerText.trim();
      const text = item.innerText;
      
      // Extract Diamond Price
      const diamondMatch = text.match(/Diamond\s*\$([\d.]+)/);
      const diamondPrice = diamondMatch ? diamondMatch[1] : 'N/A';
      
      if (diamondPrice === 'N/A') return;

      // Brand
      let brand = 'Unknown';
      if (title.toLowerCase().includes('iphone')) brand = 'Apple';
      else if (title.toLowerCase().includes('samsung')) brand = 'Samsung';
      else if (title.toLowerCase().includes('oppo')) brand = 'OPPO';
      
      // Part Type
      let partType = 'Other';
      if (title.toLowerCase().includes('screen') || title.toLowerCase().includes('lcd') || title.toLowerCase().includes('oled')) partType = 'Screen';
      else if (title.toLowerCase().includes('battery')) partType = 'Battery';
      
      // Quality/Tier - look for common ones
      const qualityKeywords = ['BQ7', 'AS NEW', 'ASSEMBLED', 'SP', 'Service Pack', 'REFURB', 'PULL', 'AMPLUS', 'HD+', 'AMP', 'Greencell'];
      let quality = 'Standard';
      for (const kw of qualityKeywords) {
        if (title.includes(kw) || title.toUpperCase().includes(kw.toUpperCase())) {
          quality = kw;
          break;
        }
      }
      
      // Model Name - try to isolate from title
      // Usually Title is: [Quality] [Part Type] for [Model] ...
      // Or: [Model] [Part Type] ...
      let model = title;
      // Remove Part Type and Brand and Quality from title to get a cleaner model name if possible
      // But user wants "Full Model Name", so I'll keep it mostly intact but cleaner.
      
      products.push({
        brand,
        model,
        partType,
        quality,
        price: diamondPrice
      });
    });
    return products;
  }
  
  const results = extractData();
  return results;
})();
