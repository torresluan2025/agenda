function showForm(formName) {
        document.getElementById('login-form').classList.remove('active');
        document.getElementById('register-form').classList.remove('active');
        document.getElementById(formName + '-form').classList.add('active');
        document.getElementById('login-tab-button').classList.remove('active');
        document.getElementById('register-tab-button').classList.remove('active');
        document.getElementById(formName + '-tab-button').classList.add('active');
      }
      function setActiveTab(buttonId) {
        // This function is called by the "Already have an account?" / "Don't have an account?" buttons
        // to ensure the correct tab is highlighted when switching forms via these links.
        document.getElementById('login-tab-button').classList.remove('active');
        document.getElementById('register-tab-button').classList.remove('active');
        document.getElementById(buttonId).classList.add('active');
      }
