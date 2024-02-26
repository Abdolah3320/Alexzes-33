
function choose_file(id) {
    document.getElementById(id).click();
};
function show(arrow, id) {
    var all = document.getElementsByClassName('files');
    var all2 = document.querySelectorAll('.sub .fa');
    var elem = document.getElementById(id);
    if (elem.style.display === 'none') {
        for (var i = 0; i < all.length; i++) {
            all[i].style.display = 'none';
            all2[i].style.rotate = '0deg'
        }
        elem.style.display = 'flex';
        arrow.style.rotate = '90deg'
    } else {
        elem.style.display = 'none';
        arrow.style.rotate = '0deg';
    }
};
function addFile(input, route) {
    var file = input.files[0];
    var req = new XMLHttpRequest();
    var formData = new FormData();
    formData.append('file', file)
    req.open('POST', route)
    req.send(formData)
    req.onreadystatechange = function () {
        if (req.readyState === 4) {
            if (req.status === 200) {
                var x = req.response
                var json = JSON.parse(x)
                if (json.error) {
                    alert('Error while uploading the file')
                } else {
                    window.location.reload()
                }
            } else {
                alert('Error: ' + req.status);
            }
        }
    }
}
function startRemove(id) {
    window.todelete = []
    var files = document.querySelectorAll(`#${id} .fl span input`)
    var arrows = document.querySelectorAll(`#${id} .fl span .fa.fa-arrow-up-right-from-square`)
    var form_del = document.querySelector(`#${id} div.form_del`)
    var form = document.querySelector(`#${id} div.form`)
    files.forEach(e => {
        e.style.display = ''
        e.checked = false
    });
    arrows.forEach(e => {
        e.style.display = 'none'
    });
    form_del.style.display = 'flex'
    form.style.display = 'none'
}
function doneRemove(id, route) {
    var ids = window.todelete
    var req = new XMLHttpRequest();
    var formData = new FormData();
    formData.append('ids', ids)
    req.open('POST', route)
    req.send(formData)
    req.onreadystatechange = function () {
        if (req.readyState === 4) {
            if (req.status === 200) {
                var x = req.response
                var json = JSON.parse(x)
                if (json.error) {
                    alert('Error while uploading the file')
                } else {
                    window.location.reload()
                    window.todelete = []
                }
            } else {
                alert('Error: ' + req.status);
            }
        }
    }
}
function addToRemove(id, elem) {
    if (elem.checked == true){
        window.todelete = [...window.todelete, id]
    } else {
        try{
            window.todelete.splice(window.todelete.indexOf(id), 1)
        }catch{}
    }
    // console.log(window.todelete)
}
function CancelRemove(id) {
    var files = document.querySelectorAll(`#${id} .fl span input`)
    var arrows = document.querySelectorAll(`#${id} .fl span .fa.fa-arrow-up-right-from-square`)
    var form_del = document.querySelector(`#${id} div.form_del`)
    var form = document.querySelector(`#${id} div.form`)
    files.forEach(e => {
        e.style.display = 'none'
    });
    arrows.forEach(e => {
        e.style.display = ''
        e.checked = false
    });
    form_del.style.display = 'none'
    form.style.display = 'flex'
    window.todelete = []
}
function sendAddSub(frm, route) {
    var ids = window.todelete
    var req = new XMLHttpRequest();
    var formData = new FormData(frm);
    req.open('POST', route)
    req.send(formData)
    req.onreadystatechange = function () {
        if (req.readyState === 4) {
            if (req.status === 200) {
                var x = req.response
                var json = JSON.parse(x)
                if (json.error) {
                    alert('Error while uploading the file')
                } else {
                    window.location.reload()
                    window.todelete = []
                }
            } else {
                alert('Error: ' + req.status);
            }
        }
    }
}
try { document.querySelector('.fa.fa-caret-down').click() } catch { }