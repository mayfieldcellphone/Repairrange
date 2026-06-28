import axios from 'axios';
import * as cheerio from 'cheerio';

export const scrapeWebsite = async (url: string) => {
    try {
        // 1. Fetch the HTML
        const { data } = await axios.get(url, {
            headers: {
                'User-Agent': 'BizHub-AI-Bot/1.0'
            }
        });

        // 2. Parse the text
        const $ = cheerio.load(data);
        
        // Remove scripts and styles
        $('script, style, nav, footer').remove();

        const title = $('title').text();
        const description = $('meta[name="description"]').attr('content') || "";
        const bodyText = $('body').text().replace(/\s+/g, ' ').trim().substring(0, 5000);

        return {
            title,
            description,
            bodyText,
            url
        };
    } catch (error: any) {
        console.error("Scraper Error:", error.message);
        return { error: "Could not reach the website. Please check the URL." };
    }
};

export const analyzeBusinessNature = async (scrapedData: any, aiModel: any) => {
    const prompt = `
        ANALYZE THIS WEBSITE DATA:
        Title: ${scrapedData.title}
        Description: ${scrapedData.description}
        Content Snippet: ${scrapedData.bodyText}
        
        TASK:
        1. Determine the "Business Nature" (e.g., Service, E-commerce, SaaS, Blog).
        2. Identify the top 3 services or products.
        3. Suggest which BizHub modules to enable: [MODULE_LEAD_GEN, MODULE_ORDERS, MODULE_FINANCE].
        
        RETURN JSON ONLY:
        {
            "nature": "...",
            "top_items": ["...", "...", "..."],
            "recommended_modules": ["...", "..."],
            "suggested_tone": "Professional/Friendly/Expert"
        }
    `;

    const result = await aiModel.generateContent(prompt);
    return JSON.parse(result.response.text());
};
