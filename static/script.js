// ==========================================
// E-COMMERCE ANALYTICS DASHBOARD
// ==========================================

let monthlyChart = null;
let categoryChart = null;
let cityChart = null;
let paymentChart = null;


// ==========================================
// FORMAT CURRENCY
// ==========================================

function formatCurrency(value) {

    return "₹" + Number(value).toLocaleString("en-IN", {
        maximumFractionDigits: 2
    });

}


// ==========================================
// GET FILTER VALUES
// ==========================================

function getFilterQuery() {

    const category =
        document.getElementById("categoryFilter").value;

    const city =
        document.getElementById("cityFilter").value;

    const fromDate =
        document.getElementById("fromDate").value;

    const toDate =
        document.getElementById("toDate").value;


    const params = new URLSearchParams();


    if (category !== "All") {

        params.append(
            "category",
            category
        );

    }


    if (city !== "All") {

        params.append(
            "city",
            city
        );

    }


    if (fromDate) {

        params.append(
            "from_date",
            fromDate
        );

    }


    if (toDate) {

        params.append(
            "to_date",
            toDate
        );

    }


    const query = params.toString();


    return query
        ? "?" + query
        : "";

}


// ==========================================
// LOAD COMPLETE DASHBOARD
// ==========================================

function loadDashboard() {

    const query = getFilterQuery();

    loadSummary(query);

    loadMonthlySales(query);

    loadCategorySales(query);

    loadCitySales(query);

    loadPaymentMethods(query);

    loadTopProducts(query);

    loadTopCustomers(query);

}


// ==========================================
// SUMMARY
// ==========================================

function loadSummary(query) {

    fetch("/api/summary" + query)

        .then(response => response.json())

        .then(data => {

            document.getElementById(
                "revenue"
            ).textContent =
                formatCurrency(data.revenue);


            document.getElementById(
                "orders"
            ).textContent =
                Number(data.orders)
                    .toLocaleString("en-IN");


            document.getElementById(
                "customers"
            ).textContent =
                Number(data.customers)
                    .toLocaleString("en-IN");


            document.getElementById(
                "average-order"
            ).textContent =
                formatCurrency(
                    data.average_order
                );

        })

        .catch(error => {

            console.error(
                "Summary error:",
                error
            );

        });

}


// ==========================================
// MONTHLY SALES
// ==========================================

function loadMonthlySales(query) {

    fetch("/api/monthly-sales" + query)

        .then(response => response.json())

        .then(data => {

            const months =
                data.map(
                    item => item.month
                );


            const revenue =
                data.map(
                    item => item.revenue
                );


            if (monthlyChart) {

                monthlyChart.destroy();

            }


            monthlyChart = new Chart(

                document.getElementById(
                    "monthlySalesChart"
                ),

                {

                    type: "line",

                    data: {

                        labels: months,

                        datasets: [

                            {

                                label: "Revenue",

                                data: revenue,

                                borderWidth: 3,

                                tension: 0.3,

                                fill: false

                            }

                        ]

                    },

                    options: {

                        responsive: true,

                        scales: {

                            y: {

                                beginAtZero: true

                            }

                        }

                    }

                }

            );

        })

        .catch(error => {

            console.error(
                "Monthly sales error:",
                error
            );

        });

}


// ==========================================
// CATEGORY SALES
// ==========================================

function loadCategorySales(query) {

    fetch("/api/category-sales" + query)

        .then(response => response.json())

        .then(data => {

            const categories =
                data.map(
                    item => item.category
                );


            const revenue =
                data.map(
                    item => item.revenue
                );


            if (categoryChart) {

                categoryChart.destroy();

            }


            categoryChart = new Chart(

                document.getElementById(
                    "categorySalesChart"
                ),

                {

                    type: "doughnut",

                    data: {

                        labels: categories,

                        datasets: [

                            {

                                label: "Revenue",

                                data: revenue,

                                borderWidth: 1

                            }

                        ]

                    },

                    options: {

                        responsive: true,

                        plugins: {

                            legend: {

                                position: "bottom"

                            }

                        }

                    }

                }

            );

        })

        .catch(error => {

            console.error(
                "Category sales error:",
                error
            );

        });

}


// ==========================================
// CITY SALES
// ==========================================

function loadCitySales(query) {

    fetch("/api/city-sales" + query)

        .then(response => response.json())

        .then(data => {

            const cities =
                data.map(
                    item => item.city
                );


            const revenue =
                data.map(
                    item => item.revenue
                );


            if (cityChart) {

                cityChart.destroy();

            }


            cityChart = new Chart(

                document.getElementById(
                    "citySalesChart"
                ),

                {

                    type: "bar",

                    data: {

                        labels: cities,

                        datasets: [

                            {

                                label: "Revenue",

                                data: revenue,

                                borderWidth: 1

                            }

                        ]

                    },

                    options: {

                        responsive: true,

                        indexAxis: "y",

                        scales: {

                            x: {

                                beginAtZero: true

                            }

                        }

                    }

                }

            );

        })

        .catch(error => {

            console.error(
                "City sales error:",
                error
            );

        });

}


// ==========================================
// PAYMENT METHODS
// ==========================================

function loadPaymentMethods(query) {

    fetch("/api/payment-methods" + query)

        .then(response => response.json())

        .then(data => {

            const methods =
                data.map(
                    item => item.method
                );


            const orders =
                data.map(
                    item => item.orders
                );


            if (paymentChart) {

                paymentChart.destroy();

            }


            paymentChart = new Chart(

                document.getElementById(
                    "paymentChart"
                ),

                {

                    type: "bar",

                    data: {

                        labels: methods,

                        datasets: [

                            {

                                label: "Orders",

                                data: orders,

                                borderWidth: 1

                            }

                        ]

                    },

                    options: {

                        responsive: true,

                        scales: {

                            y: {

                                beginAtZero: true

                            }

                        }

                    }

                }

            );

        })

        .catch(error => {

            console.error(
                "Payment methods error:",
                error
            );

        });

}


// ==========================================
// TOP PRODUCTS
// ==========================================

function loadTopProducts(query) {

    fetch("/api/top-products" + query)

        .then(response => response.json())

        .then(data => {

            const table =
                document.getElementById(
                    "products-table"
                );


            // Clear old results
            table.innerHTML = "";


            data.forEach(
                (product, index) => {

                    const row =
                        document.createElement(
                            "tr"
                        );


                    row.innerHTML = `

                        <td>
                            ${index + 1}
                        </td>

                        <td>
                            ${product.product}
                        </td>

                        <td>
                            ${Number(
                                product.quantity
                            ).toLocaleString("en-IN")}
                        </td>

                        <td>
                            ${formatCurrency(
                                product.revenue
                            )}
                        </td>

                    `;


                    table.appendChild(row);

                }
            );

        })

        .catch(error => {

            console.error(
                "Top products error:",
                error
            );

        });

}


// ==========================================
// TOP CUSTOMERS
// ==========================================

function loadTopCustomers(query) {

    fetch("/api/top-customers" + query)

        .then(response => response.json())

        .then(data => {

            const table =
                document.getElementById(
                    "customers-table"
                );


            // Clear old results
            table.innerHTML = "";


            data.forEach(
                (customer, index) => {

                    const row =
                        document.createElement(
                            "tr"
                        );


                    row.innerHTML = `

                        <td>
                            ${index + 1}
                        </td>

                        <td>
                            ${customer.customer}
                        </td>

                        <td>
                            ${customer.city}
                        </td>

                        <td>
                            ${customer.orders}
                        </td>

                        <td>
                            ${formatCurrency(
                                customer.spending
                            )}
                        </td>

                    `;


                    table.appendChild(row);

                }
            );

        })

        .catch(error => {

            console.error(
                "Top customers error:",
                error
            );

        });

}


// ==========================================
// APPLY FILTERS
// ==========================================

document.getElementById(
    "applyFilters"
).addEventListener(
    "click",
    function () {

        const fromDate =
            document.getElementById(
                "fromDate"
            ).value;

        const toDate =
            document.getElementById(
                "toDate"
            ).value;


        // Validate dates
        if (
            fromDate &&
            toDate &&
            fromDate > toDate
        ) {

            alert(
                "From Date cannot be later than To Date."
            );

            return;

        }


        loadDashboard();

    }
);


// ==========================================
// RESET FILTERS
// ==========================================

document.getElementById(
    "resetFilters"
).addEventListener(
    "click",
    function () {

        document.getElementById(
            "categoryFilter"
        ).value = "All";


        document.getElementById(
            "cityFilter"
        ).value = "All";


        document.getElementById(
            "fromDate"
        ).value = "";


        document.getElementById(
            "toDate"
        ).value = "";


        loadDashboard();

    }
);


// ==========================================
// INITIAL DASHBOARD LOAD
// ==========================================

document.addEventListener(
    "DOMContentLoaded",
    function () {

        loadDashboard();

    }
);