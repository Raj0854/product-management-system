const products_container = document.getElementById("products-container");
const search_input = document.getElementById("search-input")
const actions_btn = document.getElementById("actions-btn");
const action_dropdown = document.getElementById("action-dropdown");
const add_product_btn = document.getElementById("add-product-btn");
const add_product_form = document.getElementById("add-product-form");
const add_product_image = document.getElementById("add-product-image");

let product_data = [];
// DROPDOWN
actions_btn.addEventListener("click", () => {
    action_dropdown.classList.toggle("show");
})
// SEARCH FILTER
search_input.addEventListener("input", () => {
    const search_value = search_input.value.toLowerCase().trim();
    const filtered_Products = product_data.filter(product =>
        product.name.toLowerCase().includes(search_value) ||
        product.category.toLowerCase().includes(search_value)
    );
    display_products(filtered_Products);
})
//  add product form layout
add_product_btn.addEventListener("click", () => {
    add_product_form.classList.toggle("show")
})
// fetching product
fetch("http://127.0.0.1:5000/products")
    .then(response => response.json())
    .then(products => {
        product_data = products;
        display_products(product_data)
    })
    .catch(error => {
        console.log(error);
    });
function display_products(products) {
    products_container.innerHTML = "";
    products.forEach(product => {
        const product_card = document.createElement("div");
        product_card.classList.add("product_card")
        product_card.innerHTML = `
                <img src="${product.image || "https://via.placeholder.com/300x200?text=No+Image"}" alt="${product.name}">
                <h1>Name :${product.name}</h1>
                <p> Category :${product.category}</p>
                <h3>Price : ${product.price}</h3>
            `
        products_container.appendChild(product_card)
    })
};
// post 
const save_product_btn = document.getElementById("post-product-btn");
const product_name = document.getElementById("add-product-name");
const product_category = document.getElementById("add-product-category");
const product_price = document.getElementById("add-product-price");
save_product_btn.addEventListener("click", () => {

    const form_data = new FormData();

    form_data.append("name", product_name.value);
    form_data.append("category", product_category.value);
    form_data.append("price", product_price.value);
    form_data.append("image", add_product_image.files[0]);

    fetch("http://127.0.0.1:5000/products", {
        method: "POST",
        body: form_data
    })
        .then(response => response.json())
        .then(data => {
            console.log(data);
        })
        .catch(error => {
            console.log(error);
        });

});

const put_product_btn = document.getElementById("update-btn");

const update_product_form = document.getElementById("update-product-form");
const put = document.getElementById("put-product-btn");
const update_product_name = document.getElementById("update-product-name");
const update_product_category = document.getElementById("update-product-category");
const update_product_image = document.getElementById("update-product-image");
const update_product_price = document.getElementById("update-product-price");
const update_product_id = document.getElementById("update-product-id");
put_product_btn.addEventListener("click", () => {
    update_product_form.classList.toggle("show")
});
put.addEventListener("click", () => {

    const form_data = new FormData();

    form_data.append("id", update_product_id.value);
    form_data.append("name", update_product_name.value);
    form_data.append("category", update_product_category.value);
    form_data.append("price", update_product_price.value);
    form_data.append("image", update_product_image.files[0]);
    console.log(update_product_id.value, update_product_name.value, update_product_category.value, update_product_price.value, update_product_image.files[0]);
        // fetch("http://127.0.0.1:5000/products", {
        //     method: "PUT",
        //     body: form_data
        // })
        //     .then(response => response.json())
        //     .then(data => {
        //         console.log(data);
        //     })
        //     .catch(error => {
        //         console.log(error);
        //     });
});