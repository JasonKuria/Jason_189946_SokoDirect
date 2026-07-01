
      // Get Search Form and Page Links for Pagination to Preserve Search Query
      let searchForm = document.getElementById('searchForm')
      let pageLinks = document.getElementsByClassName('page-link')

      // Check if a search query exists in the URL
      if(searchForm) {
        for (let i=0; pageLinks.length > i; i++){
            pageLinks[i].addEventListener('click', function (e) {
              e.preventDefault() // Prevent default link behavior
              //console.log('Button Click')

              //Get the data attribute for the page number from the clicked link
              let page = this.dataset.page // This will not work as expected because 'this' does not refer to the clicked element in this context. We need to use 'e.target' instead.
              //console.log('Page:', page)

              // Add hidden input to the search form with the page number              let hiddenInput = document.createElement('input')
              searchForm.innerHTML += `<input type="hidden" name="page" value="${page}">`

              // Submit the search form
              searchForm.submit()
            })
        }

      }
