$(function(){
var app = new Vue({
  el: '#app',
  data: {
    loading: false,
    status: false,
    clientNames: [],
    clientName: '',
    description: '',
    title: '',
    priority: '',
    targetDate: '',
    products: [],
    product: '',
  },
  methods: {
    onSubmit: function(event) {
      this.loading = true
      console.log(event)
      event.target.submit()
    }
  },
  mounted(){
      this.loading=true
      console.log('called')
      SendToServer('get-request-data', 'GET', this)
      $('.field select').dropdown();
      this.loading=false
  },
  delimiters: ['$[', ']$']
})
})
var SendToServer = function(url, method, component, data={}){
  const csrfToken = getCookie('csrftoken');
  const headers = new Headers({
    "Accept": "application/json",
    "X-CSRF-TOKEN": csrfToken,
  })
  fetch(`/${url}/`, method === 'POST'?{
      method: "PUT", // *GET, POST, PUT, DELETE, etc.
      // mode: "same-origin", // no-cors, cors, *same-origin
      // cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
      credentials: "same-origin", // include, *same-origin, omit
      headers,
      // redirect: "follow", // manual, *follow, error
      // referrer: "no-referrer", // no-referrer, *client
      body: JSON.stringify(data)
      }:{})
      .then(function(response) {
        return response.json();
      })
      .then(function(myJson) {
        component.clientNames = myJson.clients;
        if (component.clientNames.length > 0){
          component.clientName = component.clientNames[0].id
        }
        component.products = myJson.products;
        component.product = component.products[0][0]
      });
  return
}
function getCookie(name) {
  if (!document.cookie) {
      return null;
  }
  const token = document.cookie.split(';')
      .map(c => c.trim())
      .filter(c => c.startsWith(name + '='));

  if (token.length === 0) {
      return null;
  }
  return decodeURIComponent(token[0].split('=')[1]);
}
