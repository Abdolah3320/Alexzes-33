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


function copyText(txt) {
    try {
        navigator.clipboard.writeText(txt)
        var icon = document.querySelector(`#${txt} .cls .fa`),
            icon2 = document.getElementById('done')
        if (icon2) {
            icon2.className = 'fa fa-copy'
            icon2.id = ''
        }
        icon.className = 'fa fa-check'
        icon.id = 'done'
    } catch {
        alert("error during copying the text")
    }
}

function show2(elm) {
    try {
        var toShow = document.getElementById('form')
        toShow.reset()
    } catch {
        try {
            var toShow = document.getElementById('form_class')
            toShow.reset()
        } catch {
            var toShow = document.getElementById('form_class_code')
            toShow.reset()
        }
    }
    toShow.style.display = 'grid'
    elm.style.display = 'none'
}
function hide2(id, elm) {
    try {
        var toHide = document.getElementById('form')
        toHide.reset()
    } catch {
        try {
            var toHide = document.getElementById('form_class')
            toHide.reset()
        } catch {
            var toHide = document.getElementById('form_class_code')
            toHide.reset()
        }
    }
    toHide.style.display = 'none'
    elm.style.display = ''
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
function submitNewGrade(form) {
    var req = new XMLHttpRequest(), formdata = new FormData(form),
        link = document.getElementById('url_new_g').href
    req.open('POST', link)

    req.onreadystatechange = function () {
        if (req.readyState == 4 && req.status == 200) {
            try {
                var json = JSON.parse(req.responseText);
                if (json.exist == 1) {
                    handleError(json.error, form)
                    unStopAll()
                } else {
                    location.reload()
                }
            } catch {
                handleError('Internal Server Error', form)
                unStopAll()
            }
        }
    }
    req.send(formdata)
}
try {
    var g_form = document.getElementById('form')
    g_form.addEventListener('submit', function (ev) {
        stopAll()
        ev.preventDefault()
        submitNewGrade(this)
    })

} catch {
    try {
        var g_form = document.getElementById('form_class')
        g_form.addEventListener('submit', function (ev) {
            stopAll()
            ev.preventDefault()
            submitNewGrade(this)
        })
    } catch {
    }
}