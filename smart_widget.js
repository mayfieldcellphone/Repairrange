/* 
  REPAIRHUB SMART CHAT WIDGET 
  This script creates a custom chat bubble that sends messages to WhatsApp 
  with a brand-specific tag so it shows up clearly in your Birdeye Inbox.
*/

(function() {
    const CONFIG = {
        'selfrepairkit.com.au': {
            name: 'SelfRepairKit AI',
            tag: '[SelfRepairKit Sale]',
            color: '#25d366',
            message: 'Hi! I am interested in a DIY repair kit.'
        },
        'mayfieldphonerepair.com.au': {
            name: 'Mayfield Repair Bot',
            tag: '[Mayfield Shop Lead]',
            color: '#007bff',
            message: 'Hi! I need a quote for a phone repair.'
        },
        'repairbill.shop': {
            name: 'RepairBill Assistant',
            tag: '[RepairBill Billing]',
            color: '#6f42c1',
            message: 'Hi! I have a question about my invoice.'
        }
    };

    const domain = window.location.hostname;
    const settings = CONFIG[domain] || CONFIG['mayfieldphonerepair.com.au'];

    // Create the Floating Button
    const button = document.createElement('div');
    button.id = 'smart-chat-btn';
    button.innerHTML = '💬 Chat';
    button.style = `
        position:fixed; bottom:20px; right:20px; 
        padding:15px 25px; background:${settings.color}; color:white; 
        border-radius:30px; cursor:pointer; font-weight:bold; 
        box-shadow: 0 4px 10px rgba(0,0,0,0.2); z-index:9999;
    `;

    button.onclick = function() {
        const phone = "15556634858"; // Your Meta Business Number
        const encodedText = encodeURIComponent(`${settings.tag} ${settings.message}`);
        window.open(`https://wa.me/${phone}?text=${encodedText}`, '_blank');
    };

    document.body.appendChild(button);
})();
