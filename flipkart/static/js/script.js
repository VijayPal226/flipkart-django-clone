document.addEventListener("DOMContentLoaded", function () {

    const wishlistButtons =
        document.querySelectorAll(".wishlist-btn");

    wishlistButtons.forEach(function (button) {

        button.addEventListener("click", function () {

            const productId =
                button.dataset.productId;

            if (!productId) {
                console.error("Product ID not found");
                return;
            }

            fetch(`/wishlist/toggle/${productId}/`, {
                method: "GET",
                headers: {
                    "X-Requested-With": "XMLHttpRequest"
                }
            })

            .then(function (response) {

                if (!response.ok) {
                    throw new Error(
                        "HTTP Error: " + response.status
                    );
                }

                return response.json();
            })

            .then(function (data) {

                console.log("Wishlist response:", data);

                if (!data.success) {
                    return;
                }

                // =========================
                // Button
                // =========================

                const icon =
                    button.querySelector("i");

                const text =
                    button.querySelector(".wishlist-text");


                if (data.added) {

                    // Heart filled
                    if (icon) {
                        icon.classList.remove("fa-regular");
                        icon.classList.add("fa-solid");
                    }

                    // Text
                    if (text) {
                        text.textContent = "Added";
                    }

                    // Button color
                    button.classList.remove(
                        "btn-outline-danger"
                    );

                    button.classList.add(
                        "btn-danger"
                    );

                } else {

                    // Heart empty
                    if (icon) {
                        icon.classList.remove("fa-solid");
                        icon.classList.add("fa-regular");
                    }

                    // Text
                    if (text) {
                        text.textContent = "Wishlist";
                    }

                    // Button color
                    button.classList.remove(
                        "btn-danger"
                    );

                    button.classList.add(
                        "btn-outline-danger"
                    );
                }


                // =========================
                // Navbar Wishlist Count
                // =========================

                const badge =
                    document.getElementById(
                        "wishlist-count-badge"
                    );


                if (badge) {

                    const count =
                        data.wishlist_count;

                    badge.textContent = count;


                    if (count > 0) {

                        badge.classList.remove(
                            "d-none"
                        );

                    } else {

                        badge.classList.add(
                            "d-none"
                        );
                    }
                }

            })

            .catch(function (error) {

                console.error(
                    "Wishlist AJAX Error:",
                    error
                );

            });

        });

    });

});