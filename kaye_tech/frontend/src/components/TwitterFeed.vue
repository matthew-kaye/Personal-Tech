<template>
  <div
    class="hastagify_embed"
    data-width="400"
    data-mode="popular"
    data-popular-type="last-week"
    data-popular-lang="en"
  >
    <div>
      <a href="http://hashtagify.me/popular"></a>
    </div>
  </div>
</template>

<script>
export default {
  name: "TwitterFeed",
  mounted() {
    const plugin = document.createElement("script");
    plugin.setAttribute("src", "//hashtagify.me/assets/hashtagify/embed.js");
    plugin.async = true;
    document.head.appendChild(plugin);
  }
};
</script>