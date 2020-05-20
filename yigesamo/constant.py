#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: yigesamo\constant.py
# Author: MingshiCai i@unoiou.com
# Date: 2020-05-19 16:27:19
HTML = """<!--// '_' //-->
<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="initial-scale=1.0" />
  <title>CNKI to Refman</title>
</head>

<body style="padding: 40px; font-family: 'Times New Roman'">
  <h3>
    CNKI to Refman/RIS<sup><small>1</small></sup> Converter<sup><small>2</small></sup>
  </h3>
  <br><br><br>
  <form method="post" name="upload_form">
    <label for="file_upload">1. Select a CNKI ref file.</label>
    <input type="file" name="file" accept=".txt" id="file_upload" />
    <br><br>
    <label for="upload_btn">2. Upload to convert</label>
    <input type="submit" value="upload" id="upload_btn" />
  </form>
  <div style="position: absolute; bottom: 40px;">
    <hr />
    <p>
      <small><sup>1</sup>https://en.wikipedia.org/wiki/RIS_(file_format)</small>
    </p>
    <p>
      <small><sup>2</sup>https://github.com/cmsax/cnki-converter</small>
    </p>
    <p>
      <small><sup>*</sup>Notice that file will be deleted after 30 seconds.</small>
    </p>
    <p>
      <small>current version: vVERSION</small>
    </p>
  </div>
</body>
<script>
  const form = document.querySelector('form')
  const submitHandler = e => {
    e.preventDefault()
    const file = document.querySelector('[type=file]').files[0]
    const formData = new FormData()
    formData.append('file', file)
    fetch('converter', { method: 'POST', body: formData }).then(res => {
      window.location = res.url
    })
  }
  form.addEventListener('submit', submitHandler, false)
</script>
</html>
"""
