// Loads data from the route /findTipologie 
fetchTipologieByLuogo('/findTipologie').then(function(res) {
    return res.json()
  }).then(function(json) {
    const inner = document.getElementById('tipologia')
    // Use the JSON data to populate these elements
    inner.innerHTML = json.nome 
  }).catch(function(err) {
    console.log(err.message)
  })