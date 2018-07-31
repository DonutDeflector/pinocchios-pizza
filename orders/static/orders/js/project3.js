document.addEventListener("DOMContentLoaded", () => {
  // fetches csrf token
  // http://musings.tinbrain.net/blog/2015/aug/28/vanilla-js-meets-djangos-csrf/
  function parse_cookies() {
    var cookies = {};
    if (document.cookie && document.cookie !== "") {
      document.cookie.split(";").forEach(function(c) {
        var m = c.trim().match(/(\w+)=(.*)/);
        if (m !== undefined) {
          cookies[m[1]] = decodeURIComponent(m[2]);
        }
      });
    }
    return cookies;
  }

  var cookies = parse_cookies();

  //
  // ordering
  //

  // AJAX request sent to add selected item cart
  document.querySelectorAll(".menu-item").forEach(element => {
    element.addEventListener("click", () => {
      const item_id = element.dataset.item_id;

      const request = new XMLHttpRequest();

      request.open("POST", "/shopping_cart_items");
      request.setRequestHeader("X-CSRFToken", cookies["csrftoken"]);

      request.onload = () => {
        // parse data, extract item quantity
        const data = JSON.parse(request.responseText);
        const quantity = data["quantity"];

        // set popup message title and content
        const title = "Success!";
        const content = "Item added to cart.";

        generate_popup_message(title, content);
        display_shopping_cart_quantity(quantity);
      };

      const data = JSON.stringify({
        item_id: item_id
      });

      request.send(data);
    });
  });

  //
  // shopping cart navbar
  //

  // fetches shopping cart item quantity if the element to display it exists
  if (document.querySelector("#shopping-cart-quantity")) {
    const request = new XMLHttpRequest();

    request.open("POST", "/shopping_cart_items");
    request.setRequestHeader("X-CSRFToken", cookies["csrftoken"]);

    request.onload = () => {
      // parse data, extract item quantity
      const data = JSON.parse(request.responseText);
      const quantity = data["quantity"];

      // call function to display number of items in the cart
      display_shopping_cart_quantity(quantity);
    };

    request.send();
  }

  // displays quantity of items in shopping cart
  function display_shopping_cart_quantity(quantity) {
    document.querySelector("#shopping-cart-quantity").innerHTML = quantity;
  }

  //
  // shopping cart
  //

  //
  // popup message
  //

  function generate_popup_message(title, content) {
    const popup_message_container = document.querySelector(
      "#popup-message-container"
    );

    const popup_message_template = Handlebars.compile(
      document.querySelector("#popup-message-template").innerHTML
    );

    const popup_message = popup_message_template({
      title: title,
      content: content
    });

    // add popup message to container, raise z-index and opacity for
    // visibility
    popup_message_container.innerHTML += popup_message;
    popup_message_container.style.zIndex = 100000;
    popup_message_container.style.opacity = 1;

    // add event listener to fade out and remove popup message
    document
      .querySelector("#popup-message-close")
      .addEventListener("click", () => {
        popup_message_container.style.zIndex = -1;
        popup_message_container.style.opacity = 0;
        document.querySelector("#popup-message").remove();
      });
  }
});
