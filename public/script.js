document.getElementById('provisionForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const vmName = document.getElementById('vm_name').value;
    const resourceGroup = document.getElementById('resource_group').value;
    const location = document.getElementById('location').value;
    const userId = document.getElementById('user_id').value;
    const recipientId = document.getElementById('recipient_id').value;

    fetch('/provision-vm', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ vm_name: vmName, resource_group: resourceGroup, location: location, user_id: userId, recipient_id: recipientId })
    })
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error('Error:', error));
});
