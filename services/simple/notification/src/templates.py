style = """
<style type="text/css">
    body {width: 600px;margin: 0 auto;}
    table {border-collapse: collapse;}
    table, td {mso-table-lspace: 0pt;mso-table-rspace: 0pt;}
    img {-ms-interpolation-mode: bicubic;}
  </style>
<![endif]-->
      <style type="text/css">
    body, p, div {
      font-family: georgia,serif;
      font-size: 14px;
    }
    body {
      color: #000000;
    }
    body a {
      color: #1188E6;
      text-decoration: none;
    }
    p { margin: 0; padding: 0; }
    table.wrapper {
      width:100% !important;
      table-layout: fixed;
      -webkit-font-smoothing: antialiased;
      -webkit-text-size-adjust: 100%;
      -moz-text-size-adjust: 100%;
      -ms-text-size-adjust: 100%;
    }
    img.max-width {
      max-width: 100% !important;
    }
    .column.of-2 {
      width: 50%;
    }
    .column.of-3 {
      width: 33.333%;
    }
    .column.of-4 {
      width: 25%;
    }
    ul ul ul ul  {
      list-style-type: disc !important;
    }
    ol ol {
      list-style-type: lower-roman !important;
    }
    ol ol ol {
      list-style-type: lower-latin !important;
    }
    ol ol ol ol {
      list-style-type: decimal !important;
    }
    @media screen and (max-width:480px) {
      .preheader .rightColumnContent,
      .footer .rightColumnContent {
        text-align: left !important;
      }
      .preheader .rightColumnContent div,
      .preheader .rightColumnContent span,
      .footer .rightColumnContent div,
      .footer .rightColumnContent span {
        text-align: left !important;
      }
      .preheader .rightColumnContent,
      .preheader .leftColumnContent {
        font-size: 80% !important;
        padding: 5px 0;
      }
      table.wrapper-mobile {
        width: 100% !important;
        table-layout: fixed;
      }
      img.max-width {
        height: auto !important;
        max-width: 100% !important;
      }
      a.bulletproof-button {
        display: block !important;
        width: auto !important;
        font-size: 80%;
        padding-left: 0 !important;
        padding-right: 0 !important;
      }
      .columns {
        width: 100% !important;
      }
      .column {
        display: block !important;
        width: 100% !important;
        padding-left: 0 !important;
        padding-right: 0 !important;
        margin-left: 0 !important;
        margin-right: 0 !important;
      }
      .social-icon-column {
        display: inline-block !important;
      }
    }
  </style>
"""
def create_html_email(**kwargs):
    title = kwargs.get("title", "Message from HealMe")
    message = kwargs.get("message", "You have a new message from HealMe")

    template = f"""
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
    <html data-editor-version="2" class="sg-campaigns" xmlns="http://www.w3.org/1999/xhtml">
        <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, minimum-scale=1, maximum-scale=1">
        <!--[if !mso]><!-->
        <meta http-equiv="X-UA-Compatible" content="IE=Edge">
        <!--<![endif]-->
        <!--[if (gte mso 9)|(IE)]>
        <xml>
            <o:OfficeDocumentSettings>
            <o:AllowPNG/>
            <o:PixelsPerInch>96</o:PixelsPerInch>
            </o:OfficeDocumentSettings>
        </xml>
        <![endif]-->
        <!--[if (gte mso 9)|(IE)]>
            {style}
        <!--user entered Head Start--><!--End Head user entered-->
        </head>
        <body>
        <center class="wrapper" data-link-color="#1188E6" data-body-style="font-size:14px; font-family:georgia,serif; color:#000000; background-color:#FFFFFF;">
            <div class="webkit">
            <table cellpadding="0" cellspacing="0" border="0" width="100%" class="wrapper" bgcolor="#FFFFFF">
                <tr>
                <td valign="top" bgcolor="#FFFFFF" width="100%">
                    <table width="100%" role="content-container" class="outer" align="center" cellpadding="0" cellspacing="0" border="0">
                    <tr>
                        <td width="100%">
                        <table width="100%" cellpadding="0" cellspacing="0" border="0">
                            <tr>
                            <td>
                                <!--[if mso]>
        <center>
        <table><tr><td width="600">
    <![endif]-->
                                        <table width="100%" cellpadding="0" cellspacing="0" border="0" style="width:100%; max-width:600px;" align="center">
                                        <tr>
                                            <td role="modules-container" style="padding:0px 0px 0px 0px; color:#000000; text-align:left;" bgcolor="#ffffff" width="100%" align="left"><table class="module preheader preheader-hide" role="module" data-type="preheader" border="0" cellpadding="0" cellspacing="0" width="100%" style="display: none !important; mso-hide: all; visibility: hidden; opacity: 0; color: transparent; height: 0; width: 0;">
        <tr>
        <td role="module-content">
            <p></p>
        </td>
        </tr>
    </table><table class="module" role="module" data-type="text" border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" data-muid="65ff2f54-7e46-437d-8b0c-d4f11d324bd5" data-mc-module-version="2019-10-22">
        <tbody>
        <tr>
            <td style="padding:20px 0px 10px 0px; line-height:14px; text-align:inherit; background-color:#FFFFFF;" height="100%" valign="top" bgcolor="#FFFFFF" role="module-content"><div><div style="font-family: inherit; text-align: center"><span style="font-size: 10px">Email not displaying correctly?</span></div>
    <div style="font-family: inherit; text-align: center"><span style="font-size: 10px; font-family: tahoma, geneva, sans-serif"><strong>View it</strong></span><span style="font-size: 10px"> in your browser.</span></div><div></div></div></td>
        </tr>
        </tbody>
    </table><table border="0" cellpadding="0" cellspacing="0" align="center" width="100%" role="module" data-type="columns" style="padding:20px 80px 40px 80px;" bgcolor="#F9F1CF" data-distribution="1">
        <tbody>
        <tr role="module-content">
            <td height="100%" valign="top"><table width="100" style="width:100px; border-spacing:0; border-collapse:collapse; margin:0px 170px 0px 170px;" cellpadding="0" cellspacing="0" align="left" border="0" bgcolor="" class="column column-0">
        <tbody>
            <tr>
            <td style="padding:0px;margin:0px;border-spacing:0;"><table class="wrapper" role="module" data-type="image" border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" data-muid="727c6539-81ff-45f6-8ec1-bdddfdc64758">
        <tbody>
        <tr>
            <td style="font-size:6px; line-height:10px; padding:0px 0px 0px 0px;" valign="top" align="center">
            <img class="max-width" border="0" style="display:block; color:#000000; text-decoration:none; font-family:Helvetica, arial, sans-serif; font-size:16px; max-width:100% !important; width:100%; height:auto !important;" width="100" alt="" data-proportionally-constrained="true" data-responsive="true" src="https://i.imgur.com/LFQcPe9.png">
            </td>
        </tr>
        </tbody>
    </table></td>
            </tr>
        </tbody>
        </table></td>
        </tr>
        </tbody>
    </table><table border="0" cellpadding="0" cellspacing="0" align="center" width="100%" role="module" data-type="columns" style="padding:0px 0px 30px 0px;" bgcolor="#F9F1CF" data-distribution="1">
        <tbody>
        <tr role="module-content">
            <td height="100%" valign="top"><table width="500" style="width:500px; border-spacing:0; border-collapse:collapse; margin:0px 50px 0px 50px;" cellpadding="0" cellspacing="0" align="left" border="0" bgcolor="" class="column column-0">
        <tbody>
            <tr>
            <td style="padding:0px;margin:0px;border-spacing:0;"><table class="module" role="module" data-type="text" border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" data-muid="88b10083-1ced-4e2e-b2cb-dde1536068eb.1" data-mc-module-version="2019-10-22">
        <tbody>
        <tr>
            <td style="padding:0px 0px 0px 0px; line-height:30px; text-align:inherit;" height="100%" valign="top" bgcolor="" role="module-content"><div><div style="font-family: inherit; text-align: center"><span style="font-family: tahoma, geneva, sans-serif; font-size: 30px"><strong>{title}</strong></span></div><div></div></div></td>
        </tr>
        </tbody>
    </table></td>
            </tr>
        </tbody>
        </table></td>
        </tr>
        </tbody>
    </table><table class="wrapper" role="module" data-type="image" border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" data-muid="a63532d0-90ab-4cc6-89b8-0a24da35ee24">
        <tbody>
        <tr>
            <td style="font-size:6px; line-height:10px; padding:0px 0px 0px 0px;" valign="top" align="center">
            <img class="max-width" border="0" style="display:block; color:#000000; text-decoration:none; font-family:Helvetica, arial, sans-serif; font-size:16px; max-width:100% !important; width:100%; height:auto !important;" width="600" alt="" data-proportionally-constrained="true" data-responsive="true" src="http://cdn.mcauto-images-production.sendgrid.net/c31721ac5f4f8b45/6e36ed9e-6514-4093-97c5-a1ebddb1d936/1913x989.jpg">
            </td>
        </tr>
        </tbody>
    </table><table class="module" role="module" data-type="divider" border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" data-muid="446188b1-8134-4a30-a5bd-24d357ccb73e">
        <tbody>
        <tr>
            <td style="padding:10px 0px 10px 0px;" role="module-content" height="100%" valign="top" bgcolor="">
            <table border="0" cellpadding="0" cellspacing="0" align="center" width="100%" height="1px" style="line-height:1px; font-size:1px;">
                <tbody>
                <tr>
                    <td style="padding:0px 0px 1px 0px;" bgcolor="#a1a1a1"></td>
                </tr>
                </tbody>
            </table>
            </td>
        </tr>
        </tbody>
    </table><table border="0" cellpadding="0" cellspacing="0" align="center" width="100%" role="module" data-type="columns" style="padding:0px 10px 0px 10px;" bgcolor="#E5F2E5" data-distribution="1">
        <tbody>
        <tr role="module-content">
            <td height="100%" valign="top"><table width="480" style="width:480px; border-spacing:0; border-collapse:collapse; margin:0px 50px 0px 50px;" cellpadding="0" cellspacing="0" align="left" border="0" bgcolor="" class="column column-0">
        <tbody>
            <tr>
            <td style="padding:0px;margin:0px;border-spacing:0;"><table class="module" role="module" data-type="text" border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" data-muid="d37e1f74-e5e6-4c5b-9d69-14d90c8e0a52" data-mc-module-version="2019-10-22">
        <tbody>
        <tr>
            <td style="padding:30px 0px 30px 0px; line-height:30px; text-align:inherit; background-color:#E5F2E5;" height="100%" valign="top" bgcolor="#E5F2E5" role="module-content"><div><div style="font-family: inherit; text-align: center"><span style="font-size: 20px"><em>{message}</em></span></div>
        </tr>
        </tbody>
    </table></td>
            </tr>
        </tbody>
        </table></td>
        </tr>
        </tbody>
    </table><table class="module" role="module" data-type="divider" border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" data-muid="446188b1-8134-4a30-a5bd-24d357ccb73e.1.1">
        <tbody>
        <tr>
            <td style="padding:10px 0px 10px 0px;" role="module-content" height="100%" valign="top" bgcolor="">
            <table border="0" cellpadding="0" cellspacing="0" align="center" width="100%" height="1px" style="line-height:1px; font-size:1px;">
                <tbody>
                <tr>
                    <td style="padding:0px 0px 1px 0px;" bgcolor="#a1a1a1"></td>
                </tr>
                </tbody>
            </table>
            </td>
        </tr>
        </tbody>
    </table><table border="0" cellpadding="0" cellspacing="0" align="center" width="100%" role="module" data-type="columns" style="padding:20px 0px 20px 0px;" bgcolor="#F9F1CF" data-distribution="1">
        <tbody>
        <tr role="module-content">
            <td height="100%" valign="top"><table width="600" style="width:600px; border-spacing:0; border-collapse:collapse; margin:0px 0px 0px 0px;" cellpadding="0" cellspacing="0" align="left" border="0" bgcolor="" class="column column-0">
        <tbody>
            <tr>
            <td style="padding:0px;margin:0px;border-spacing:0;"><table border="0" cellpadding="0" cellspacing="0" class="module" data-role="module-button" data-type="button" role="module" style="table-layout:fixed;" width="100%" data-muid="46cefa58-9ccf-4a83-978b-1b135f330ca2">
        <tbody>
            <tr>
            <td align="center" bgcolor="" class="outer-td" style="padding:0px 0px 0px 0px;">
                <table border="0" cellpadding="0" cellspacing="0" class="wrapper-mobile" style="text-align:center;">
                <tbody>
                    <tr>
                    <td align="center" bgcolor="#ffffff" class="inner-td" style="border-radius:6px; font-size:16px; text-align:center; background-color:inherit;">
                    <a href="http://localhost:8080" style="background-color:#ffffff; border:0px solid #333333; border-color:#333333; border-radius:0px; border-width:0px; color:#000000; display:inline-block; font-size:12px; font-weight:700; letter-spacing:0px; line-height:normal; padding:15px 30px 15px 30px; text-align:center; text-decoration:none; border-style:solid; font-family:tahoma,geneva,sans-serif;" target="_blank">Open HealMe</a>
                    </td>
                    </tr>
                </tbody>
                </table>
            </td>
            </tr>
        </tbody>
        </table></td>
            </tr>
        </tbody>
        </table></td>
        </tr>
        </tbody>
    </table><table border="0" cellpadding="0" cellspacing="0" align="center" width="100%" role="module" data-type="columns" style="padding:0px 0px 0px 0px;" bgcolor="#FFFFFF" data-distribution="1,1,1">
        <tbody>
        <tr role="module-content">
            <td height="100%" valign="top"><table width="186" style="width:186px; border-spacing:0; border-collapse:collapse; margin:0px 10px 0px 0px;" cellpadding="0" cellspacing="0" align="left" border="0" bgcolor="" class="column column-0">
        <tbody>
            <tr>
            <td style="padding:0px;margin:0px;border-spacing:0;"><table class="wrapper" role="module" data-type="image" border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" data-muid="2c9c2635-0c87-48f0-aae4-e8e502e0066d">
        <tbody>
        <tr>
            <td style="font-size:6px; line-height:10px; padding:0px 0px 0px 0px;" valign="top" align="center">
            <img class="max-width" border="0" style="display:block; color:#000000; text-decoration:none; font-family:Helvetica, arial, sans-serif; font-size:16px; max-width:100% !important; width:100%; height:auto !important;" width="186" alt="" data-proportionally-constrained="true" data-responsive="true" src="http://cdn.mcauto-images-production.sendgrid.net/c31721ac5f4f8b45/52494f55-9a99-44ed-a607-84735c832f7d/888x1647.jpg">
            </td>
        </tr>
        </tbody>
    </table></td>
            </tr>
        </tbody>
        </table><table width="186" style="width:186px; border-spacing:0; border-collapse:collapse; margin:0px 10px 0px 10px;" cellpadding="0" cellspacing="0" align="left" border="0" bgcolor="" class="column column-1">
        <tbody>
            <tr>
            <td style="padding:0px;margin:0px;border-spacing:0;"><table class="module" role="module" data-type="text" border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" data-muid="ac4bdf03-c785-4fc8-8f02-fad752709d77" data-mc-module-version="2019-10-22">
        <tbody>
        <tr>
            <td style="padding:50px 0px 20px 0px; line-height:22px; text-align:inherit;" height="100%" valign="top" bgcolor="" role="module-content"><div><div style="font-family: inherit; text-align: center"><span style="font-size: 18px; font-family: tahoma, geneva, sans-serif"><strong>OUR SERVICES</strong></span></div><div></div></div></td>
        </tr>
        </tbody>
    </table><table class="module" role="module" data-type="text" border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" data-muid="d61d6c93-24ed-43c0-a931-d1b581afb26b" data-mc-module-version="2019-10-22">
        <tbody>
        <tr>
            <td style="padding:0px 0px 0px 0px; line-height:22px; text-align:inherit;" height="100%" valign="top" bgcolor="" role="module-content"><div><div style="font-family: inherit; text-align: center"><span style="font-size: 16px"><em>Online and onsite appointments&nbsp;</em></span></div><div></div></div></td>
        </tr>
        </tbody>
    </table><table class="module" role="module" data-type="divider" border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" data-muid="61828c88-a31e-4a79-8497-b667b47dfeaa.1">
        <tbody>
        <tr>
            <td style="padding:10px 50px 10px 50px;" role="module-content" height="100%" valign="top" bgcolor="">
            <table border="0" cellpadding="0" cellspacing="0" align="center" width="100%" height="1px" style="line-height:1px; font-size:1px;">
                <tbody>
                <tr>
                    <td style="padding:0px 0px 1px 0px;" bgcolor="#A1A1A1"></td>
                </tr>
                </tbody>
            </table>
            </td>
        </tr>
        </tbody>
    </table><table class="module" role="module" data-type="text" border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" data-muid="d61d6c93-24ed-43c0-a931-d1b581afb26b.1.1" data-mc-module-version="2019-10-22">
        <tbody>
        <tr>
            <td style="padding:0px 0px 0px 0px; line-height:22px; text-align:inherit;" height="100%" valign="top" bgcolor="" role="module-content"><div><div style="font-family: inherit; text-align: center"><span style="font-size: 16px"><em>Lab tests</em></span></div><div></div></div></td>
        </tr>
        </tbody>
    </table><table class="module" role="module" data-type="divider" border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" data-muid="61828c88-a31e-4a79-8497-b667b47dfeaa.2">
        <tbody>
        <tr>
            <td style="padding:10px 50px 10px 50px;" role="module-content" height="100%" valign="top" bgcolor="">
            <table border="0" cellpadding="0" cellspacing="0" align="center" width="100%" height="1px" style="line-height:1px; font-size:1px;">
                <tbody>
                <tr>
                    <td style="padding:0px 0px 1px 0px;" bgcolor="#A1A1A1"></td>
                </tr>
                </tbody>
            </table>
            </td>
        </tr>
        </tbody>
    </table><table class="module" role="module" data-type="text" border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" data-muid="d61d6c93-24ed-43c0-a931-d1b581afb26b.1.2" data-mc-module-version="2019-10-22">
        <tbody>
        <tr>
            <td style="padding:0px 0px 0px 0px; line-height:22px; text-align:inherit;" height="100%" valign="top" bgcolor="" role="module-content"><div><div style="font-family: inherit; text-align: center"><span style="font-size: 16px"><em>Wellness checks</em></span></div><div></div></div></td>
        </tr>
        </tbody>
    </table><table class="module" role="module" data-type="divider" border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" data-muid="61828c88-a31e-4a79-8497-b667b47dfeaa">
        <tbody>
        <tr>
            <td style="padding:10px 50px 10px 50px;" role="module-content" height="100%" valign="top" bgcolor="">
            <table border="0" cellpadding="0" cellspacing="0" align="center" width="100%" height="1px" style="line-height:1px; font-size:1px;">
                <tbody>
                <tr>
                    <td style="padding:0px 0px 1px 0px;" bgcolor="#A1A1A1"></td>
                </tr>
                </tbody>
            </table>
            </td>
        </tr>
        </tbody>
    </table><table class="module" role="module" data-type="text" border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" data-muid="d61d6c93-24ed-43c0-a931-d1b581afb26b.1" data-mc-module-version="2019-10-22">
        <tbody>
        <tr>
            <td style="padding:0px 0px 32px 0px; line-height:22px; text-align:inherit;" height="100%" valign="top" bgcolor="" role="module-content"><div><div style="font-family: inherit; text-align: center"><span style="font-size: 16px"><em>Prescriptions</em></span></div><div></div></div></td>
        </tr>
        </tbody>
    </table></td>
            </tr>
        </tbody>
        </table><table width="186" style="width:186px; border-spacing:0; border-collapse:collapse; margin:0px 0px 0px 10px;" cellpadding="0" cellspacing="0" align="left" border="0" bgcolor="" class="column column-2">
        <tbody>
            <tr>
            <td style="padding:0px;margin:0px;border-spacing:0;"><table class="wrapper" role="module" data-type="image" border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" data-muid="02bb3363-f0bc-4059-bb11-0d5e1023afb3">
        <tbody>
        <tr>
            <td style="font-size:6px; line-height:10px; padding:0px 0px 0px 0px;" valign="top" align="center">
            <img class="max-width" border="0" style="display:block; color:#000000; text-decoration:none; font-family:Helvetica, arial, sans-serif; font-size:16px; max-width:100% !important; width:100%; height:auto !important;" width="186" alt="" data-proportionally-constrained="true" data-responsive="true" src="http://cdn.mcauto-images-production.sendgrid.net/c31721ac5f4f8b45/ab64aab3-3432-406f-96ae-a9760536b841/888x1647.jpg">
            </td>
        </tr>
        </tbody>
    </table></td>
            </tr>
        </tbody>
        </table></td>
        </tr>
        </tbody>
    </table><table class="module" role="module" data-type="text" border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" data-muid="b5c8b557-ace1-405a-b573-f272688df4b5" data-mc-module-version="2019-10-22">
        <tbody>
        <tr>
            <td style="padding:40px 0px 0px 0px; line-height:16px; text-align:inherit; background-color:#E5F2E5;" height="100%" valign="top" bgcolor="#E5F2E5" role="module-content"><div><div style="font-family: inherit; text-align: center"><span style="font-family: tahoma, geneva, sans-serif; font-size: 12px">1824 Fillmore Street, Phoenix, Arizona, 85408</span></div>
    <div style="font-family: inherit; text-align: center"><span style="font-family: tahoma, geneva, sans-serif; font-size: 12px">480.299.3149</span></div><div></div></div></td>
        </tr>
        </tbody>
    </table><table class="module" role="module" data-type="social" align="center" border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" data-muid="ae833234-0741-4995-a39b-3c916cf05fff">
        <tbody>
        <tr>
            <td valign="top" style="padding:20px 0px 40px 0px; font-size:6px; line-height:10px; background-color:#E5F2E5;" align="center">
            <table align="center" style="-webkit-margin-start:auto;-webkit-margin-end:auto;">
                <tbody><tr align="center"><td style="padding: 0px 5px;" class="social-icon-column">
        <a role="social-icon-link" href="https://www.facebook.com/sendgrid/" target="_blank" alt="Facebook" title="Facebook" style="display:inline-block; background-color:#000000; height:25px; width:25px;">
            <img role="social-icon" alt="Facebook" title="Facebook" src="https://mc.sendgrid.com/assets/social/white/facebook.png" style="height:25px; width:25px;" height="25" width="25">
        </a>
        </td><td style="padding: 0px 5px;" class="social-icon-column">
        <a role="social-icon-link" href="https://twitter.com/sendgrid" target="_blank" alt="Twitter" title="Twitter" style="display:inline-block; background-color:#000000; height:25px; width:25px;">
            <img role="social-icon" alt="Twitter" title="Twitter" src="https://mc.sendgrid.com/assets/social/white/twitter.png" style="height:25px; width:25px;" height="25" width="25">
        </a>
        </td><td style="padding: 0px 5px;" class="social-icon-column">
        <a role="social-icon-link" href="https://www.instagram.com/sendgrid/" target="_blank" alt="Instagram" title="Instagram" style="display:inline-block; background-color:#000000; height:25px; width:25px;">
            <img role="social-icon" alt="Instagram" title="Instagram" src="https://mc.sendgrid.com/assets/social/white/instagram.png" style="height:25px; width:25px;" height="25" width="25">
        </a>
        </td><td style="padding: 0px 5px;" class="social-icon-column">
        <a role="social-icon-link" href="https://www.pinterest.com/sendgrid/" target="_blank" alt="Pinterest" title="Pinterest" style="display:inline-block; background-color:#000000; height:25px; width:25px;">
            <img role="social-icon" alt="Pinterest" title="Pinterest" src="https://mc.sendgrid.com/assets/social/white/pinterest.png" style="height:25px; width:25px;" height="25" width="25">
        </a>
        </td><td style="padding: 0px 5px;" class="social-icon-column">
        <a role="social-icon-link" href="https://www.linkedin.com/company/sendgrid/" target="_blank" alt="LinkedIn" title="LinkedIn" style="display:inline-block; background-color:#000000; height:25px; width:25px;">
            <img role="social-icon" alt="LinkedIn" title="LinkedIn" src="https://mc.sendgrid.com/assets/social/white/linkedin.png" style="height:25px; width:25px;" height="25" width="25">
        </a>
        </td></tr></tbody>
            </table>
            </td>
        </tr>
        </tbody>
    </table>
        <tbody>
            <tr>
            <td align="center" bgcolor="" class="outer-td" style="padding:20px 0px 20px 0px;">
                <table border="0" cellpadding="0" cellspacing="0" class="wrapper-mobile" style="text-align:center;">
                <tbody>
                    <tr>
                    <td align="center" bgcolor="#F5F8FD" class="inner-td" style="border-radius:6px; font-size:16px; text-align:center; background-color:inherit;">
                    <a href="https://sendgrid.com/" style="background-color:#F5F8FD; border:1px solid #F5F8FD; border-color:#F5F8FD; border-radius:25px; border-width:1px; color:#A8B9D5; display:inline-block; font-size:10px; font-weight:normal; letter-spacing:0px; line-height:normal; padding:5px 18px 5px 18px; text-align:center; text-decoration:none; border-style:solid; font-family:helvetica,sans-serif;" target="_blank">♥ POWERED BY TWILIO SENDGRID</a>
                    </td>
                    </tr>
                </tbody>
                </table>
            </td>
            </tr>
        </tbody>
        </table></td>
                                        </tr>
                                        </table>
                                        <!--[if mso]>
                                    </td>
                                    </tr>
                                </table>
                                </center>
                                <![endif]-->
                            </td>
                            </tr>
                        </table>
                        </td>
                    </tr>
                    </table>
                </td>
                </tr>
            </table>
            </div>
        </center>
        </body>
    </html>

    """
    return template