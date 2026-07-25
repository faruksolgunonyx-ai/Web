/**
 * Bright Data Web Scraper IDE - Legal Text Extraction Engine
 * Environment: Browser Context (DOM access required)
 */

module.exports = {
  navigate: async function () {
    // Wait exactly 2000ms to ensure dynamic DOM nodes (like SPAs) have settled.
    await new Promise(resolve => setTimeout(resolve, 2000));
    return true;
  },

  parse: function () {
    // 1. Extract raw visible text. 
    // Fallback to empty string if the body is somehow null or inaccessible.
    let rawText = document.body.innerText || "";

    // 2. Clean excessive whitespace immediately to normalize the data.
    let cleanedText = rawText.replace(/\s+/g, ' ').trim();

    let maskedCount = 0;

    // 3. Define strict regex patterns for PII masking.
    const patterns = [
      {
        name: "EMAIL",
        regex: /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b/gi,
        replacement: "[EMAIL]"
      },
      {
        name: "PHONE",
        // Covers international formats, optional country codes, spaces, dots, dashes.
        regex: /\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b/g,
        replacement: "[PHONE]"
      },
      {
        name: "IP",
        regex: /\b(?:\d{1,3}\.){3}\d{1,3}\b/g,
        replacement: "[IP]"
      },
      {
        name: "CREDIT_CARD",
        // Matches 13-16 digits, allowing for common space or dash separators.
        regex: /\b(?:\d[ -]*?){13,16}\b/g,
        replacement: "[CREDIT_CARD]"
      },
      {
        name: "IBAN",
        // Standard IBAN format: 2 letters, 2 digits, up to 30 alphanumeric chars.
        regex: /\b[A-Z]{2}[0-9]{2}(?:[ ]?[0-9a-zA-Z]){11,28}\b/g,
        replacement: "[IBAN]"
      }
    ];

    // 4. Apply masking BEFORE truncation.
    patterns.forEach(pattern => {
      cleanedText = cleanedText.replace(pattern.regex, () => {
        maskedCount++;
        return pattern.replacement;
      });
    });

    // 5. Truncate strictly to the first 10,000 characters.
    const fullText = cleanedText.substring(0, 10000);

    // 6. Generate text preview (first 500 characters of the final text).
    const textPreview = fullText.substring(0, 500);

    // 7. Calculate word count securely (handling empty strings).
    const wordCount = fullText.length > 0 ? fullText.split(/\s+/).length : 0;

    // 8. Construct and return the exact required payload.
    return {
      url: window.location.href,
      full_text: fullText,
      text_preview: textPreview,
      word_count: wordCount,
      masked_count: maskedCount,
      extraction_timestamp: new Date().toISOString()
    };
  }
};
