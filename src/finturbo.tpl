<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>$if(title)$$title$$else$Finturbo Research Report$endif$</title>
  <style>
    /* ==== 摩根大通核心配色 ==== */
    :root {
      --jpm-blue: #003366;  /* 摩根蓝 */
      --jpm-accent: #6699cc; /* 辅助蓝 */
      --jpm-light-bg: #f0f4f7;
    }
    
    body {
      font-family: "Helvetica Neue", Arial, sans-serif;
      line-height: 1.6;
      color: #333;
      max-width: 210mm;
      margin: 0 auto;
      padding: 15mm;
      background: white;
    }
    
    /* 标题样式 */
    h1 {
      color: var(--jpm-blue);
      font-size: 24pt;
      border-bottom: 2px solid var(--jpm-accent);
      padding-bottom: 8px;
      margin-top: 0;
    }
    
    h2 {
      color: var(--jpm-blue);
      font-size: 18pt;
      border-left: 4px solid var(--jpm-accent);
      padding-left: 10px;
      margin-top: 30px;
    }
    
    /* 表格样式（摩根风格紧凑表格） */
    table {
      width: 100%;
      border-collapse: collapse;
      margin: 20px 0;
      font-size: 10pt;
    }
    
    th {
      background-color: var(--jpm-light-bg);
      color: var(--jpm-blue);
      font-weight: bold;
      padding: 8px 12px;
      border-bottom: 2px solid var(--jpm-accent);
    }
    
    td {
      padding: 8px 12px;
      border-bottom: 1px solid #ddd;
    }
    
    /* 代码/模型输出区块 */
    pre {
      background: var(--jpm-light-bg);
      border-left: 4px solid var(--jpm-accent);
      padding: 12px;
      overflow-x: auto;
    }
    
    /* 页脚免责声明 */
    .footer {
      margin-top: 40px;
      padding-top: 15px;
      border-top: 1px solid var(--jpm-accent);
      font-size: 9pt;
      color: #666;
    }
    
    /* 关键数据高亮 */
    .highlight {
      background-color: #e6f2ff;
      padding: 2px 4px;
      border-radius: 3px;
    }

  img.base64-image {
    max-width: 100%;
    height: auto;
    display: block;
    margin: 20px auto;
    border: 1px solid #eee;
    box-shadow: 0 2px 4px rgba(0,51,102,0.1);
  }

  /* 小尺寸图片 */
  img.base64-image.small {
    max-width: 400px;
  }

  /* 中尺寸图片 */
  img.base64-image.medium {
    max-width: 600px;
  }

  /* 大尺寸图片 */
  img.base64-image.large {
    max-width: 800px;
  }

  /* 全宽图片 */
  img.base64-image.full-width {
    width: 100%;
  }

  </style>
</head>
<body>
  <!-- 标题区 -->
  <div class="header">
    <h1>$if(title)$$title$$else$Finturbo Research Report$endif$</h1>
    $if(date)$<div class="report-date">$date$</div>$endif$
  </div>
  
  <!-- 报告主体 -->

  <!-- TABLE_PLACEHOLDER -->

  <!-- IMAGE_PLACEHOLDER -->

  $body$
  
  <!-- 页脚 -->
  <div class="footer">
    <strong>Finturbo Disclaimer:</strong> This material is for informational purposes only. 
  </div>
</body>
</html>