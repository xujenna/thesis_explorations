var nodemailer = require('nodemailer');

var transporter = nodemailer.createTransport({
  service: 'gmail',
  auth: {
    user: 'fitterhappierbot@gmail.com',
    pass: 'G3z@f3vw'
  }
});


function emailContent(subject, text){
    let body = ""
    if(typeof text == "object"){
        text.forEach(d=>{
            body += (d + "\n")
        })
    }
    else{
        body = text
    }
    var mailOptions = {
        from: 'Fitter Happier <fitterhappierbot@gmail.com>',
        to: 'xujenna@gmail.com',
        subject: subject,
        text: body
      };
    transporter.sendMail(mailOptions, function(error, info){
        if (error) {
            console.log(error);
        } else {
            console.log('Email sent: ' + info.response);
        }
    });
}


module.exports = {
    emailContent: emailContent
}