module.exports = function(eleventyConfig) {
  // Passthrough copy: static assets that don't need processing
  eleventyConfig.addPassthroughCopy("styles.css");
  eleventyConfig.addPassthroughCopy("ga4-events.js");
  eleventyConfig.addPassthroughCopy("images");
  eleventyConfig.addPassthroughCopy("CNAME");
  eleventyConfig.addPassthroughCopy(".nojekyll");
  eleventyConfig.addPassthroughCopy("robots.txt");
  eleventyConfig.addPassthroughCopy("sitemap.xml");

  // Watch targets for live reload during development
  eleventyConfig.addWatchTarget("styles.css");
  eleventyConfig.addWatchTarget("images/");

  // Ignore markdown source files that conflict with existing HTML
  // (e.g., blog/*.md when blog/*.html already exists)
  eleventyConfig.ignores.add("blog/*.md");
  eleventyConfig.ignores.add("news/*.md");
  eleventyConfig.ignores.add(".agents/");

  // HTML files without frontmatter are auto-passthrough-copied (not skipped)
  eleventyConfig.addPassthroughCopy("news/");
  eleventyConfig.addPassthroughCopy("blog/");
  eleventyConfig.addPassthroughCopy("stories/");
  eleventyConfig.addPassthroughCopy("treatments/");
  // Passthrough copy: root-level HTML files that should be served as-is
  // (index.html, about.html, cancer.html, etc. — not processed by 11ty)
  // Use glob to avoid copying the _site/ output directory itself
  const glob = require("glob");
  glob.sync("*.html").forEach(file => eleventyConfig.addPassthroughCopy(file));

  return {
    dir: {
      input: ".",
      output: "_site",
      includes: "_includes",
      layouts: "_layouts",
      data: "_data"
    },
    htmlTemplateEngine: "njk",
    markdownTemplateEngine: "njk",
    templateFormats: ["njk", "md"]
  };
};
