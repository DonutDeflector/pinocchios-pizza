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

      request.open("POST", "/add_item_to_cart");
      request.setRequestHeader("X-CSRFToken", cookies["csrftoken"]);

      request.onload = () => {
        // parse data, extract item quantity
        const data = JSON.parse(request.responseText);
        const quantity = data["quantity"];
        const total_price = data["total_price"];

        // set popup message title and content
        const title = "Success!";
        const content = "Item added to cart.";

        generate_popup_message(title, content);
        display_shopping_cart_quantity(quantity);
        display_shopping_cart_total_price(total_price);
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

  // displays total price of items in shopping cart
  function display_shopping_cart_total_price(total_price) {
    document.querySelector(".shopping-cart-total-price-amount").innerHTML =
      "$" + total_price;
  }

  //
  // shopping cart
  //

  if (document.querySelector(".btn-item-remove")) {
    document.querySelectorAll(".btn-item-remove").forEach(element => {
      element.addEventListener("click", () => {
        const item_number = element.dataset.item_number;
        const item_type = element.dataset.item_type;

        const request = new XMLHttpRequest();

        request.open("POST", "/remove_item_from_cart");
        request.setRequestHeader("X-CSRFToken", cookies["csrftoken"]);

        request.onload = () => {
          // parse data, extract item number
          const data = JSON.parse(request.responseText);
          const quantity = data["quantity"];
          const total_price = data["total_price"];

          const item = $(
            `.shopping-cart-item[data-item_number=${item_number}][data-item_type=${item_type}]`
          );

          item.remove();

          // set popup message title and content
          const title = "Success!";
          const content = "Item removed from cart.";

          generate_popup_message(title, content);
          display_shopping_cart_quantity(quantity);
          display_shopping_cart_total_price(total_price);
        };

        const data = JSON.stringify({
          item_number: item_number,
          item_type: item_type
        });

        request.send(data);
      });
    });
  }

  //
  // customize pizza
  //

  // get the price of the pizza on page load
  fetch_pizza_price();

  // when the form is altered, fetch the price of the pizza
  $("#pizza-form :input").change(() => {
    fetch_pizza_price();
  });

  // check for existence of submit, adds the configured pizza to the user's cart
  if (document.querySelector("#pizza-submit-button")) {
    document
      .querySelector("#pizza-submit-button")
      .addEventListener("click", () => {
        // capture category, size, and toppings of configured pizza
        pizza = fetch_configured_pizza();

        const request = new XMLHttpRequest();

        request.open("POST", "/add_pizza_to_cart");
        request.setRequestHeader("X-CSRFToken", cookies["csrftoken"]);

        request.onload = () => {
          // parse data, extract item quantity
          const data = JSON.parse(request.responseText);
          const quantity = data["quantity"];
          const total_price = data["total_price"];

          // set popup message title and content
          const title = "Success!";
          const content = "Pizza added to cart.";

          generate_popup_message(title, content);
          display_shopping_cart_quantity(quantity);
          display_shopping_cart_total_price(total_price);
        };

        const data = JSON.stringify({
          pizza_category: pizza.category,
          pizza_size: pizza.size,
          pizza_toppings: pizza.toppings
        });

        request.send(data);

        // reset pizza topping selection status
        const topping_checkboxes = document.querySelectorAll(".pizza-topping");
        for (topping_checkbox in topping_checkboxes) {
          topping_checkboxes[topping_checkbox].checked = false;
        }

        // reset pizza price
        fetch_pizza_price();
      });
  }
  // gets the price of the currently configured pizza
  function fetch_pizza_price() {
    // only run if the pizza form is present
    if (document.querySelector("#pizza-form")) {
      // capture category, size, and toppings of configured pizza
      pizza = fetch_configured_pizza();

      const request = new XMLHttpRequest();

      request.open("POST", "/customize_pizza");
      request.setRequestHeader("X-CSRFToken", cookies["csrftoken"]);

      request.onload = () => {
        const data = JSON.parse(request.responseText);
        const pizza_price = data["pizza_price"];

        // display price of configured pizza
        document.querySelector(".pizza-price").innerHTML = "$" + pizza_price;
      };

      const data = JSON.stringify({
        pizza_category: pizza.category,
        pizza_size: pizza.size,
        pizza_toppings: pizza.toppings
      });

      request.send(data);
    }
  }

  // fetch category, size, and toppings of configured pizza
  function fetch_configured_pizza() {
    // fetch pizza category and size
    const pizza_category = document.querySelector("#pizza-category").value;
    const pizza_size = document.querySelector("#pizza-size").value;

    // get all toppings from the form
    const pizza_toppings = document.querySelectorAll(".pizza-topping");

    // declare an array for selected pizza toppings
    let pizza_toppings_selected = [];

    // find pizza toppings that were selected and add them to the array
    for (pizza_topping in pizza_toppings) {
      if (pizza_toppings[pizza_topping].checked) {
        pizza_toppings_selected.push(pizza_toppings[pizza_topping].value);
      }
    }

    return {
      category: pizza_category,
      size: pizza_size,
      toppings: pizza_toppings_selected
    };
  }

  //
  // customize sub
  //

  // get the price of the sub on page load
  fetch_sub_price();

  // when the form is altered, fetch the price of the pizza
  $("#sub-form :input").change(() => {
    fetch_sub_price();
  });

  // check for existence of submit, adds the configured sub to the user's cart
  if (document.querySelector("#sub-submit-button")) {
    document
      .querySelector("#sub-submit-button")
      .addEventListener("click", () => {
        // capture name, category, size, and addons of configured sub
        sub = fetch_configured_sub();

        const request = new XMLHttpRequest();

        request.open("POST", "/add_sub_to_cart");
        request.setRequestHeader("X-CSRFToken", cookies["csrftoken"]);

        request.onload = () => {
          // parse data, extract item quantity
          const data = JSON.parse(request.responseText);
          const quantity = data["quantity"];
          const total_price = data["total_price"];

          // set popup message title and content
          const title = "Success!";
          const content = "Sub added to cart.";

          generate_popup_message(title, content);
          display_shopping_cart_quantity(quantity);
          display_shopping_cart_total_price(total_price);
        };

        const data = JSON.stringify({
          sub_name: sub.name,
          sub_size: sub.size,
          sub_addons: sub.addons
        });

        request.send(data);
      });
  }

  // gets the price of the currently configured sub
  function fetch_sub_price() {
    if (document.querySelector("#sub-form")) {
    }
  }

  // fetch name, size, and addons of configured sub
  function fetch_configured_sub() {
    // fetch sub name and size
    const sub_name = document.querySelector("#sub-name").value;
    const sub_size = document.querySelector("#sub-size").value;

    // get all of the addons from the form
    const addons = document.querySelectorAll(".sub-addon");

    // declare array for selected addons
    let addons_selected = [];

    // find addons that were selected and add them to the array
    for (addon in addons) {
      if (addons[addon].checked) {
        addons_selected.push(addons[addon].value);
      }
    }

    return {
      name: sub_name,
      size: sub_size,
      addons: addons_selected
    };
  }

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
