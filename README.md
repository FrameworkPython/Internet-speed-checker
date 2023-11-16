# Internet-speed-checker-
Internet speed checker (upload, download, ping) considering the location, very accurate and fast 
```pip install python ```
<div style="background-color: blue; border: 2px solid black; padding: 10px;">
  <div style="background-color: white; border: 2px solid red; padding: 10px;">
    <pre id="code">
      # این یک کد پایتون است
      print("Hello, World!")
    </pre>
    <button onclick="copyCode()">Copy</button>
  </div>
</div>
<script>
  function copyCode() {
    // یافتن عنصر pre با شناسه code
    let code = document.getElementById("code");
    // ایجاد یک عنصر textarea برای کپی کردن متن
    let textarea = document.createElement("textarea");
    // قرار دادن متن کد در عنصر textarea
    textarea.value = code.textContent;
    // اضافه کردن عنصر textarea به صفحه
    document.body.appendChild(textarea);
    // انتخاب متن عنصر textarea
    textarea.select();
    // کپی کردن متن انتخاب شده به کلیپ‌بورد
    document.execCommand("copy");
    // حذف کردن عنصر textarea از صفحه
    document.body.removeChild(textarea);
    // تغییر متن دکمه به Copied
    let button = document.querySelector("button");
    button.textContent = "Copied";
    // بازگشت متن دکمه به Copy بعد از 2 ثانیه
    setTimeout(function() {
      button.textContent = "Copy";
    }, 2000);
  }
</script>

