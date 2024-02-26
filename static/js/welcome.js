const schoolForm = document.getElementById("school")
const teacherForm = document.getElementById("teacher")
const studentForm = document.getElementById("student")
const verifyForm = document.getElementById("verify")
const loginForm = document.getElementById('loginform');
const container = document.getElementById('container');
const registerBtn = document.getElementById('register');
const registerBtn2 = document.getElementById('reg2');
const loginBtn = document.getElementById('login');
const loginBtns = document.querySelectorAll('.login');
const div = document.getElementById("switch")
const div2 = document.getElementById("none")
verifyForm.style.display = 'none'
function encrypt(text, key) {
  let result = '';
  for (let i = 0; i < text.length; i++) {
      const charCode = text.charCodeAt(i) ^ key.charCodeAt(i % key.length);
      result += String.fromCharCode(charCode);
  }
  return result;
}
function stopAll() {
  var btns = document.querySelectorAll('button');
  btns.forEach(element => {
    element.disabled = true
  });
}
function unStopAll() {
  var btns = document.querySelectorAll('button');
  btns.forEach(element => {
    element.disabled = false
  });
}

registerBtn.addEventListener('click', () => {
  studentForm.style.display = 'flex'
  schoolForm.style.display = 'flex'
  teacherForm.style.display = 'flex'
  container.classList.add('active');
  div.style.display = "flex"
  div2.style.display = "none"
});

// registerBtn2.addEventListener('click', () => {
//   loginForm.style.display = 'none'
//   studentForm.style.display = 'flex'
//   schoolForm.style.display = 'flex'
//   teacherForm.style.display = 'flex'
//   container.classList.add('active');
//   div.style.display = "flex"
//   div2.style.display = "none"
// });

loginBtn.addEventListener('click', () => {
  loginForm.style.display = 'flex'
  studentForm.style.display = 'none'
  schoolForm.style.display = 'none'
  teacherForm.style.display = 'none'
  container.classList.remove('active');
  div.style.display = "none"
  div2.style.display = "block"
});

// loginBtns.forEach(element => {
//   element.addEventListener('click', () => {
//     loginForm.style.display = 'flex'
//     studentForm.style.display = 'none'
//     schoolForm.style.display = 'none'
//     teacherForm.style.display = 'none'
//     container.classList.remove('active');
//     div.style.display = "none"
//     div2.style.display = "block"
//   });
// })


function select(elm, css) {
  const h = document.getElementById('sel')
  const slctr = document.getElementById('selector')
  slctr.style.transform = css
  h.id = ''
  elm.id = 'sel'

}




function teacher() {
  teacherForm.style.display = "flex"
  schoolForm.style.display = "none"
  studentForm.style.display = "none"
}
function school() {
  teacherForm.style.display = "none"
  schoolForm.style.display = "flex"
  studentForm.style.display = "none"
}
function student() {
  teacherForm.style.display = "none"
  schoolForm.style.display = "none"
  studentForm.style.display = "flex"
}
function verify() {
  teacherForm.style.display = "none"
  schoolForm.style.display = "none"
  studentForm.style.display = "none"
  verifyForm.style.display = "flex"
  var tohide = document.querySelectorAll('.tohide');
  tohide.forEach(element => {
    element.style.display = "none"
  });
  document.getElementById('switch').style.display = 'none';
  unStopAll()
}

function handleError(errorMessage, form) {
  var existingError = document.getElementById('error-p');
  if (existingError) {
    form.removeChild(existingError);

  }

  var error = document.createElement('p');
  error.id = 'error-p';
  error.innerText = errorMessage;
  form.appendChild(error);
}

loginForm.addEventListener('submit', function (ev) {
  stopAll()
  ev.preventDefault();

  var data = new FormData(loginForm);

  var req = new XMLHttpRequest();

  req.open('POST', '/collectdata/login');

  req.onreadystatechange = function () {
    if (req.readyState == 4) {
      if (req.status == 200) {
        try {
          var json = JSON.parse(req.responseText);
          var id = json.id;
          if (id != 0) {
            window.location.reload()
          } else {
            handleError('Wrong Password or E-mail', loginForm);
            return unStopAll();
          }
        } catch (e) {
          handleError('Error parsing server response', loginForm);
          return unStopAll();
        }
      }
    }
  };
  req.send(data);
});

studentForm.addEventListener('submit', function (ev) {
  stopAll()
  ev.preventDefault()
  submitSignup('st-pass', 'st-pass2', studentForm, '/st/collectdata/signup')
})
schoolForm.addEventListener('submit', function (ev) {
  stopAll()
  ev.preventDefault()
  submitSignup('sc-pass', 'sc-pass2', schoolForm, '/sc/collectdata/signup')
})
teacherForm.addEventListener('submit', function (ev) {
  stopAll()
  ev.preventDefault()
  submitSignup('t-pass', 't-pass2', teacherForm, '/t/collectdata/signup')
})

function submitSignup(ps1, ps2, form, route) {
  var passval = document.getElementById(ps1).value
  var pass2 = document.getElementById(ps2)
  var passval2 = pass2.value
  pass2.style.border = 'none'
  if (passval != passval2) {
    handleError('The two passwords are not the same', form)
    pass2.style.border = 'solid 2px #e94a5d';
    pass2.value = '';
    return 0;
  }
  var formdata = new FormData(form);
  var req = new XMLHttpRequest()
  req.open('POST', route)

  req.onreadystatechange = function () {
    if (req.readyState == 4 && req.status == 200) {
      try {
        var json = JSON.parse(req.responseText);
        if (json.exist == 1) {
          handleError(json.error, form)
          unStopAll()
        } else {
          verify()
          localStorage.setItem('error', json.error)
        }
      } catch {
        handleError('Internal Server Error', form)
        unStopAll()
      }
    }
  }
  req.send(formdata)
};

verifyForm.addEventListener('submit', function (ev) {
  stopAll()
  ev.preventDefault()
  var formdata = new FormData(verifyForm);
  formdata.append('v-error', localStorage.getItem('error'))
  var req = new XMLHttpRequest()
  req.open('POST', '/get-vercode')

  req.onreadystatechange = function () {
    if (req.readyState == 4 && req.status == 200) {
      try {
        var json = JSON.parse(req.responseText);
        if (json.exist == 0) {
          handleError('Wrong Number', verifyForm)
          return unStopAll();
        } else {
          var tohide = document.querySelectorAll('.tohide');
          tohide.forEach(element => {
            element.style.display = "";
          });
          unStopAll()
          document.getElementById('login').click()
        }
      } catch {
        handleError('Internal Server Error', verifyForm)
        return unStopAll();
      }
    }
  }
  req.send(formdata)
})