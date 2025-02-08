# this is where we can define the patterns for product and category pages
# also we can use llms to learn about the product and category pages url and then define/enhance the patterns
# and since the config is in a separate file, we can easily change the patterns without changing the spider code
# this is a good example of separation of concerns
# also we can later on we can define the patterns in a database and fetch them from there
config = {
  "product_patterns": ["/product/", "/dp/", "/gp/", "/p/", "/offer/"],
  "category_patterns": ["/s?", "/b?", "/stores/", "/category/", "/collections/", "/gp/browse/"],
  "exclude_patterns": ["/cart", "/account", "/signin", "/login", "/help", "/gp/help", "/gp/cart"]
  }
