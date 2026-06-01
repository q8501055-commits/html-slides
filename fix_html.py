import re

with open(r"C:\Users\User\.openclaw\workspace\html-slides-repo\Humanoid_Robot_Tactile_Sensors_2026_Final.html", "r", encoding="utf-8") as f:
    content = f.read()

# Extract slides
slides_content = []

# Find header
header_match = re.search(r'<header>(.*?)</header>', content, re.DOTALL)
if header_match:
    slides_content.append(header_match.group(1))

# Find all divs with class slide
slide_matches = re.finditer(r'<div class="slide">(.*?)</div>', content, re.DOTALL)
for match in slide_matches:
    slides_content.append(match.group(1))

if not slides_content:
    print("No slides found! Make sure the file exists and has <div class=\"slide\"> blocks.")
    exit(1)

html_template = """<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>2026 人形機器人觸覺感測器產業白皮書</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Noto+Sans+TC:wght@300;400;700&display=swap');
        
        body, html {
            margin: 0; padding: 0; height: 100vh; width: 100vw;
            background: #050510;
            color: #0ff;
            font-family: 'Noto Sans TC', sans-serif;
            overflow: hidden;
        }

        .bg-grid {
            position: absolute; top: 0; left: 0; right: 0; bottom: 0;
            background-image: 
                linear-gradient(rgba(0, 255, 255, 0.05) 1px, transparent 1px),
                linear-gradient(90deg, rgba(0, 255, 255, 0.05) 1px, transparent 1px);
            background-size: 40px 40px;
            z-index: -1;
            transform: perspective(500px) rotateX(60deg) scale(2.5) translateY(-100px);
            animation: moveGrid 10s linear infinite;
        }

        @keyframes moveGrid {
            0% { background-position: 0 0; }
            100% { background-position: 0 40px; }
        }

        .slides-container {
            width: 100vw; height: 100vh;
            display: flex;
            transition: transform 0.6s cubic-bezier(0.25, 1, 0.5, 1);
        }

        .slide {
            min-width: 100vw; min-height: 100vh;
            display: flex; flex-direction: column;
            justify-content: center; align-items: center;
            position: relative;
            box-sizing: border-box;
            padding: 40px;
        }

        .glass-panel {
            background: rgba(10, 20, 40, 0.6);
            border: 1px solid rgba(0, 255, 255, 0.2);
            border-radius: 20px;
            padding: 50px;
            width: 90%;
            max-width: 1200px;
            max-height: 90vh;
            overflow-y: auto;
            box-shadow: 0 0 30px rgba(0, 255, 255, 0.1), inset 0 0 20px rgba(0, 255, 255, 0.05);
            backdrop-filter: blur(15px);
            animation: float 6s ease-in-out infinite;
            text-align: left;
        }
        
        .glass-panel::-webkit-scrollbar { width: 8px; }
        .glass-panel::-webkit-scrollbar-track { background: rgba(0, 255, 255, 0.05); }
        .glass-panel::-webkit-scrollbar-thumb { background: rgba(0, 255, 255, 0.3); border-radius: 4px; }

        @keyframes float {
            0% { transform: translateY(0px) rotateX(0deg); }
            50% { transform: translateY(-10px) rotateX(1deg); }
            100% { transform: translateY(0px) rotateX(0deg); }
        }

        h1, h2, h3 {
            font-family: 'Orbitron', 'Noto Sans TC', sans-serif;
            color: #fff;
            text-shadow: 0 0 10px #0ff, 0 0 20px #00aaff;
            letter-spacing: 1px;
            margin-top: 0;
            border-bottom: 1px solid rgba(0,255,255,0.3);
            padding-bottom: 15px;
        }
        
        h1 { font-size: 2.5em; text-align: center; }
        h2 { font-size: 2em; }

        p, li {
            font-size: 1.3em;
            line-height: 1.8;
            color: #e0ffff;
            text-shadow: 0 0 5px rgba(0,255,255,0.3);
        }

        .img-container {
            text-align: center; margin: 20px 0;
        }
        
        img {
            max-width: 100%; max-height: 400px;
            border-radius: 10px;
            border: 1px solid rgba(0, 255, 255, 0.4);
            box-shadow: 0 0 20px rgba(0, 255, 255, 0.2);
        }

        .controls {
            position: fixed; bottom: 20px; left: 50%;
            transform: translateX(-50%);
            z-index: 1000;
            display: flex;
            gap: 20px;
        }

        button {
            background: rgba(0, 255, 255, 0.1);
            border: 1px solid #0ff;
            color: #0ff;
            padding: 10px 25px;
            font-family: 'Orbitron', sans-serif;
            font-size: 1.2em;
            cursor: pointer;
            border-radius: 5px;
            transition: all 0.3s ease;
            box-shadow: 0 0 10px rgba(0, 255, 255, 0.2);
        }

        button:hover {
            background: rgba(0, 255, 255, 0.3);
            box-shadow: 0 0 20px rgba(0, 255, 255, 0.8);
            text-shadow: 0 0 5px #fff;
        }
        
        .progress-bar {
            position: fixed; top: 0; left: 0; height: 4px;
            background: #0ff;
            box-shadow: 0 0 10px #0ff;
            z-index: 1000;
            transition: width 0.4s ease;
        }
    </style>
</head>
<body>
    <div class="bg-grid"></div>
    <div class="progress-bar" id="progress"></div>
    
    <div class="slides-container" id="slides-container">
"""

for content_html in slides_content:
    html_template += f"""
        <div class="slide">
            <div class="glass-panel">
                {content_html}
            </div>
        </div>
"""

html_template += """
    </div>
    <div class="controls">
        <button onclick="prevSlide()">&#9664; PREV</button>
        <button onclick="nextSlide()">NEXT &#9654;</button>
    </div>

    <script>
        let currentSlide = 0;
        const slides = document.querySelectorAll('.slide');
        const totalSlides = slides.length;
        const container = document.getElementById('slides-container');
        const progress = document.getElementById('progress');

        function updateSlide() {
            container.style.transform = `translateX(-${currentSlide * 100}vw)`;
            progress.style.width = `${((currentSlide + 1) / totalSlides) * 100}%`;
        }

        function nextSlide() {
            if (currentSlide < totalSlides - 1) {
                currentSlide++;
                updateSlide();
            }
        }

        function prevSlide() {
            if (currentSlide > 0) {
                currentSlide--;
                updateSlide();
            }
        }

        document.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowRight' || e.key === ' ') nextSlide();
            if (e.key === 'ArrowLeft') prevSlide();
        });
        
        updateSlide();
    </script>
</body>
</html>
"""

with open(r"C:\Users\User\.openclaw\workspace\html-slides-repo\Humanoid_Robot_Tactile_Sensors_2026_Final.html", "w", encoding="utf-8") as f:
    f.write(html_template)

print(f"Generated successfully. Slides count: {len(slides_content)}")
