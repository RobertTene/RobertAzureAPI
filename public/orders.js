window.onload = function() {
    fetchOrders();
};

function fetchOrders() {
    // Fetch orders from the FastAPI backend and populate the ordersList div
    fetch('http://localhost:8000/orders')  // Replace with your actual FastAPI server URL if different
        .then(response => response.json())
        .then(orders => {
            const ordersList = document.getElementById('ordersList');
            let html = '<table>';
            html += '<tr><th>ID</th><th>VM Name</th><th>Resource Group</th><th>Location</th><th>User ID</th><th>Recipient ID</th><th>Status</th></tr>';
            orders.forEach(order => {
                html += `<tr>
                            <td>${order.id}</td>
                            <td>${order.vm_name}</td>
                            <td>${order.rg_name}</td>
                            <td>${order.location}</td>
                            <td>${order.user_id}</td>
                            <td>${order.recipient_id}</td>
                            <td>${order.status}</td>
                         </tr>`;
            });
            html += '</table>';
            ordersList.innerHTML = html;
        })
        .catch(error => console.error('Error fetching orders:', error));
}
