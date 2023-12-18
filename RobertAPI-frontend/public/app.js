document.getElementById('provision').addEventListener('click', function() {
  axios.get('http://localhost:8000/provision/West%20Europe/TestApi/TestVM/')
    .then(function(response) {
      console.log('Provisioned:', response.data);
    })
    .catch(function(error) {
      console.error('Error provisioning:', error);
    });
});

document.getElementById('deprovision').addEventListener('click', function() {
  axios.get('http://localhost:8000/deprovision/TestApi/TestVM/')
    .then(function(response) {
      console.log('Deprovisioned:', response.data);
    })
    .catch(function(error) {
      console.error('Error deprovisioning:', error);
    });
});
