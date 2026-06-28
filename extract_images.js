(async () => {
    const steps = document.querySelectorAll('.step');
    const results = [];
    for (let i = 0; i < 6 && i < steps.length; i++) {
        const step = steps[i];
        const title = step.querySelector('.step-title')?.textContent.trim() || `Step ${i+1}`;
        const img = step.querySelector('img');
        if (img) {
            results.push({
                step: i + 1,
                title: title,
                src: img.src,
                srcset: img.srcset
            });
        }
    }
    return results;
})()