const products_container = document.getElementById("products-container");
const search_input = document.getElementById("search-input")
const actions_btn = document.getElementById("actions-btn");
const action_dropdown = document.getElementById("action-dropdown");
const add_product_btn = document.getElementById("add-product-btn");
const product_form = document.getElementById("product-form");
const product_image = document.getElementById("product-image");

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
    product_form.classList.toggle("show")
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
const save_product_btn = document.getElementById("save-product-btn");
const product_name = document.getElementById("product-name");
const product_category = document.getElementById("product-category");
const product_price = document.getElementById("product-price");
save_product_btn.addEventListener("click", () => {

    const form_data = new FormData();

    form_data.append("name", product_name.value);
    form_data.append("category", product_category.value);
    form_data.append("price", product_price.value);
    form_data.append("image", product_image.files[0]);

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