
  //Get search form and page links 
  let searchForm = document.getElementById('searchForm')
  let pageLinks = document.getElementsByClassName('page-link')

  // Ensure Search Form exists 
  if(searchForm) {
    for(let i=0; pageLinks.length > i; i++){
      pageLinks[i].addEventListener('click',function (e){
        e.preventDefault()
        
        //GET THE DATA ATTRIBUTE
        let page = this.dataset.page

        //ADD HIDDEN SEARCH INPUT TO FORM
        searchForm.innerHTML += `<input value="${page}" name="page" hidden/>`

        //submit form
        searchForm.submit()
      })
    }
  } 