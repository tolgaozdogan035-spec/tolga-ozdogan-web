#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import re
import sys

def format_content(raw_content: str, quote: str = "") -> str:
    """Metin paragraflarını <p> etiketlerine dönüştürür ve alıntı ekler."""
    paragraphs = [p.strip() for p in raw_content.split("\n\n") if p.strip()]
    formatted_html = []
    
    for i, p in enumerate(paragraphs):
        # İlk paragrafı vurgulu yap
        if i == 0:
            formatted_html.append(
                f'<p class="text-xl md:text-2xl text-white font-serif leading-relaxed italic border-b border-brand-gray/10 pb-6">{p}</p>'
            )
        else:
            formatted_html.append(f'<p>{p}</p>')
            
        # 3. paragraftan sonra alıntı ekle (varsa)
        if i == 2 and quote:
            formatted_html.append(
                f'<div class="article-quote">\n    "{quote}"\n</div>'
            )
            
    return "\n\n".join(formatted_html)

def generate_article_page(title: str, slug: str, date_str: str, read_time: str, category: str, content_html: str, tags: list) -> str:
    """Yeni makaleye ait tam bağımsız HTML sayfasını üretir."""
    tags_html = "\n".join([
        f'<span class="text-xs font-sans bg-brand-card border border-brand-gray/20 text-brand-gray px-3 py-1 rounded-sm">{t}</span>'
        for t in tags
    ])
    
    file_name = f"yazi-{slug}.html"
    page_url = f"https://tolgaozdogan.com/{file_name}"
    
    return f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | Tolga Özdoğan</title>
    <meta name="description" content="Yazar Tolga Özdoğan'ın {title} başlıklı köşe yazısı.">
    
    <link rel="icon" type="image/png" href="./favicon.png">
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Lora:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Montserrat:wght@300;400;500;600&family=Alex+Brush&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {{
            theme: {{
                extend: {{
                    colors: {{
                        'brand-dark': '#0B0F19',
                        'brand-card': '#111724',
                        'brand-gold': '#D4AF37',
                        'brand-gray': '#A0AAB2',
                    }},
                    fontFamily: {{
                        'display': ['Cinzel', 'serif'],
                        'serif': ['Lora', 'serif'],
                        'sans': ['Montserrat', 'sans-serif'],
                        'signature': ['Alex Brush', 'cursive'],
                    }}
                }}
            }}
        }}
    </script>
    <style>
        body {{ background-color: #0B0F19; color: #E2E8F0; font-family: 'Lora', serif; line-height: 1.95; }}
        ::-webkit-scrollbar {{ width: 8px; }}
        ::-webkit-scrollbar-track {{ background: #0B0F19; }}
        ::-webkit-scrollbar-thumb {{ background: #2A3650; border-radius: 4px; }}
        ::-webkit-scrollbar-thumb:hover {{ background: #D4AF37; }}
        ::selection {{ background: #D4AF37; color: #0B0F19; }}
        .reveal {{ opacity: 0; transform: translateY(30px); transition: all 0.8s ease-out; }}
        .reveal.active {{ opacity: 1; transform: translateY(0); }}
        .article-quote {{ border-left: 3px solid #D4AF37; padding-left: 1.75rem; margin: 3rem 0; font-style: italic; color: #FFFFFF; font-size: 1.25rem; line-height: 1.8; }}
    </style>
</head>
<body class="antialiased selection:bg-brand-gold selection:text-brand-dark">

    <!-- Navbar -->
    <nav class="fixed w-full z-50 transition-all duration-300 backdrop-blur-md bg-brand-dark/95 border-b border-brand-gold/10 py-4 shadow-lg" id="navbar">
        <div class="max-w-7xl mx-auto px-6 md:px-12 flex justify-between items-center">
            <a href="index.html" class="font-signature text-3xl md:text-4xl text-brand-gold hover:text-white transition-colors tracking-wide">Tolga Özdoğan</a>
            
            <div class="hidden lg:flex space-x-6 font-sans text-xs tracking-wide items-center">
                <a href="index.html#eserler" class="text-brand-gray hover:text-brand-gold transition-colors uppercase">Eserler</a>
                <a href="index.html#yazar" class="text-brand-gray hover:text-brand-gold transition-colors uppercase">Yazar Hakkında</a>
                <a href="dusunce-defteri.html" class="text-brand-gray hover:text-brand-gold transition-colors uppercase">Düşünce Defteri</a>
                <a href="roportajlar.html" class="text-brand-gray hover:text-brand-gold transition-colors uppercase">Röportajlar</a>
                <a href="kose-yazilari.html" class="text-brand-gold font-semibold transition-colors uppercase border-b border-brand-gold pb-1">Köşe Yazıları</a>
                <a href="sosyal-medya.html" class="text-brand-gray hover:text-brand-gold transition-colors uppercase">Sosyal Medya</a>
                <a href="basin.html" class="text-brand-gray hover:text-brand-gold transition-colors uppercase">Basında Biz</a>
            </div>

            <button class="lg:hidden text-brand-gold focus:outline-none" onclick="toggleMobileMenu()">
                <i class="fas fa-bars text-2xl"></i>
            </button>
        </div>
        
        <div id="mobile-menu" class="hidden lg:hidden absolute w-full bg-brand-dark border-b border-brand-gold/20 py-4 px-6 flex flex-col space-y-4 shadow-2xl">
             <a href="index.html#eserler" class="text-white hover:text-brand-gold font-sans uppercase text-sm border-b border-brand-gray/20 pb-2">Eserler</a>
             <a href="index.html#yazar" class="text-white hover:text-brand-gold font-sans uppercase text-sm border-b border-brand-gray/20 pb-2">Yazar Hakkında</a>
             <a href="dusunce-defteri.html" class="text-white hover:text-brand-gold font-sans uppercase text-sm border-b border-brand-gray/20 pb-2">Düşünce Defteri</a>
             <a href="roportajlar.html" class="text-white hover:text-brand-gold font-sans uppercase text-sm border-b border-brand-gray/20 pb-2">Röportajlar</a>
             <a href="kose-yazilari.html" class="text-brand-gold font-sans uppercase text-sm border-b border-brand-gray/20 pb-2">Köşe Yazıları</a>
             <a href="sosyal-medya.html" class="text-white hover:text-brand-gold font-sans uppercase text-sm border-b border-brand-gray/20 pb-2">Sosyal Medya</a>
             <a href="basin.html" class="text-white hover:text-brand-gold font-sans uppercase text-sm">Basında Biz</a>
        </div>
    </nav>

    <!-- Header -->
    <header class="pt-36 pb-16 bg-gradient-to-b from-brand-dark to-[#0f1423] border-b border-brand-gold/10">
        <div class="max-w-4xl mx-auto px-6 text-center reveal active">
            <div class="mb-6 flex items-center justify-center gap-3">
                <a href="kose-yazilari.html" class="text-brand-gold hover:text-white font-sans text-xs tracking-widest uppercase transition-colors">
                    <i class="fas fa-arrow-left mr-1"></i> Köşe Yazılarına Dön
                </a>
                <span class="text-brand-gray/40">•</span>
                <span class="text-brand-gold font-sans text-xs tracking-widest uppercase border border-brand-gold/40 px-2 py-0.5 rounded-sm">
                    {category}
                </span>
            </div>

            <h1 class="font-display text-3xl md:text-4xl lg:text-5xl font-bold text-white mb-6 leading-tight">
                {title}
            </h1>
            
            <div class="w-20 h-px bg-brand-gold mx-auto mb-6"></div>

            <div class="flex flex-wrap items-center justify-center gap-4 text-brand-gray text-xs font-sans">
                <span><i class="fas fa-user-pen text-brand-gold mr-1"></i> Tolga Özdoğan</span>
                <span>•</span>
                <span><i class="far fa-calendar-alt text-brand-gold mr-1"></i> {date_str}</span>
                <span>•</span>
                <span><i class="far fa-clock text-brand-gold mr-1"></i> {read_time}</span>
            </div>
        </div>
    </header>

    <!-- İçerik -->
    <main class="py-16 bg-[#0B0F19]">
        <div class="max-w-3xl mx-auto px-6">
            <article class="font-serif text-slate-200 text-lg leading-relaxed space-y-7 reveal active">
                {content_html}
            </article>

            <!-- Etiketler ve Paylaşım -->
            <div class="mt-12 pt-8 border-t border-brand-gray/10 flex flex-col md:flex-row justify-between items-center gap-6 reveal">
                <div class="flex flex-wrap gap-2">
                    {tags_html}
                </div>

                <div class="flex items-center gap-3">
                    <span class="text-xs font-sans text-brand-gray uppercase tracking-wider">Paylaş:</span>
                    <a href="https://twitter.com/intent/tweet?text={title}&url={page_url}" target="_blank" class="w-8 h-8 rounded-full border border-brand-gray/30 flex items-center justify-center text-brand-gray hover:text-brand-dark hover:bg-brand-gold hover:border-brand-gold transition-all duration-300">
                        <i class="fab fa-x-twitter text-xs"></i>
                    </a>
                    <a href="https://www.linkedin.com/sharing/share-offsite/?url={page_url}" target="_blank" class="w-8 h-8 rounded-full border border-brand-gray/30 flex items-center justify-center text-brand-gray hover:text-brand-dark hover:bg-brand-gold hover:border-brand-gold transition-all duration-300">
                        <i class="fab fa-linkedin-in text-xs"></i>
                    </a>
                    <a href="https://api.whatsapp.com/send?text={page_url}" target="_blank" class="w-8 h-8 rounded-full border border-brand-gray/30 flex items-center justify-center text-brand-gray hover:text-brand-dark hover:bg-brand-gold hover:border-brand-gold transition-all duration-300">
                        <i class="fab fa-whatsapp text-xs"></i>
                    </a>
                </div>
            </div>

            <!-- Yazar Kutusu -->
            <div class="mt-16 bg-brand-card border border-brand-gray/10 p-8 rounded-lg flex flex-col md:flex-row items-center gap-6 shadow-xl reveal">
                <div class="w-24 h-24 flex-shrink-0 relative">
                    <div class="absolute inset-0 rounded-full border-2 border-brand-gold/30 transform -translate-x-1 -translate-y-1"></div>
                    <img src="./Tolga 2.png" alt="Yazar Tolga Özdoğan" class="w-full h-full object-cover rounded-full border-2 border-brand-card relative z-10 shadow-md">
                </div>
                <div class="text-center md:text-left space-y-2">
                    <h3 class="font-display text-xl font-bold text-white">Tolga Özdoğan</h3>
                    <p class="font-sans text-brand-gold text-xs tracking-widest uppercase">Yazar & Tasarımcı</p>
                    <p class="font-serif text-brand-gray text-sm italic leading-relaxed">
                        "Kelimelerle dünyayı yeniden kurmak, insanı en çok da kendi labirentlerinde özgürleştiren tek yoldur."
                    </p>
                </div>
            </div>

            <!-- Alt Navigasyon Butonu -->
            <div class="mt-12 text-center reveal">
                <a href="kose-yazilari.html" class="inline-flex items-center bg-brand-gold/10 border border-brand-gold/50 text-brand-gold px-8 py-3 rounded-sm font-sans text-xs tracking-widest uppercase hover:bg-brand-gold hover:text-brand-dark transition-all duration-300">
                    ← Tüm Köşe Yazılarını İncele
                </a>
            </div>
        </div>
    </main>

    <!-- Footer -->
    <footer class="bg-black py-10 border-t border-brand-gold/20">
        <div class="max-w-7xl mx-auto px-6 flex flex-col md:flex-row justify-between items-center">
            <p class="font-sans text-xs text-brand-gray/60 mb-4 md:mb-0">
                &copy; <span id="year"></span> Tolga Özdoğan. Tüm hakları saklıdır.
            </p>
            <div class="font-sans text-xs text-brand-gray/60">
                Yazar Resmi Web Sitesidir.
            </div>
        </div>
    </footer>

    <script>
        document.getElementById('year').textContent = new Date().getFullYear();
        function toggleMobileMenu() {{
            const menu = document.getElementById('mobile-menu');
            menu.classList.toggle('hidden');
        }}
        const observer = new IntersectionObserver((entries, obs) => {{
            entries.forEach(entry => {{
                if (entry.isIntersecting) {{
                    entry.target.classList.add('active');
                    obs.unobserve(entry.target);
                }}
            }});
        }}, {{ threshold: 0.15 }});
        document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
    </script>
</body>
</html>
"""

def update_kose_yazilari_list(title: str, slug: str, date_str: str, read_time: str, category: str, snippet: str, list_file_path: str = "kose-yazilari.html"):
    """kose-yazilari.html dosyasındaki liste container'ının başına yeni yazı kartını ekler."""
    if not os.path.exists(list_file_path):
        print(f"Hata: '{list_file_path}' dosyası bulunamadı.")
        sys.exit(1)

    with open(list_file_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    new_file_name = f"yazi-{slug}.html"
    
    card_html = f"""
                    <!-- Yeni Yazı: {title} -->
                    <article class="reveal bg-[#111724] border border-brand-gray/10 p-8 md:p-10 rounded-lg hover:border-brand-gold/40 transition-colors duration-300 shadow-xl">
                        <div class="flex flex-col md:flex-row md:items-center justify-between mb-6 border-b border-brand-gray/10 pb-4">
                            <div class="flex items-center gap-3 mb-4 md:mb-0">
                                <span class="text-brand-gold font-sans text-xs tracking-widest uppercase border border-brand-gold/50 px-2 py-1 rounded-sm">{category}</span>
                                <span class="text-brand-gray font-sans text-xs"><i class="far fa-calendar-alt mr-1"></i> {date_str}</span>
                            </div>
                            <span class="text-brand-gray font-sans text-xs italic">Okuma süresi: {read_time}</span>
                        </div>
                        
                        <h2 class="font-display text-2xl md:text-3xl text-white font-bold mb-6 hover:text-brand-gold transition-colors cursor-pointer" onclick="window.location.href='{new_file_name}'">{title}</h2>
                        
                        <div class="font-serif text-brand-gray text-base leading-relaxed space-y-4">
                            <p>{snippet}</p>
                        </div>
                        
                        <div class="mt-8 pt-6 text-right">
                            <a href="{new_file_name}" class="inline-flex items-center bg-brand-gold/10 border border-brand-gold/50 text-brand-gold px-6 py-2 rounded-sm font-sans text-xs tracking-widest uppercase hover:bg-brand-gold hover:text-brand-dark transition-all duration-300">
                                Yazının Devamını Oku
                            </a>
                        </div>
                    </article>
"""

    target_tag = '<div class="lg:col-span-8 space-y-12">'
    if target_tag in html_content:
        updated_content = html_content.replace(target_tag, target_tag + "\n" + card_html, 1)
        with open(list_file_path, "w", encoding="utf-8") as f:
            f.write(updated_content)
        print(f"'{list_file_path}' başarıyla güncellendi.")
    else:
        print(f"Uyarı: '{target_tag}' etiketi '{list_file_path}' içinde bulunamadı.")

def main():
    parser = argparse.ArgumentParser(description="Yeni köşe yazısı HTML sayfalarını oluşturan ve listeyi güncelleyen betik.")
    parser.add_argument("--title", required=True, help="Köşe yazısının başlığı")
    parser.add_argument("--slug", required=True, help="Yazı URL slug'ı (örn: sansurun-golgesinde-hakikat)")
    parser.add_argument("--date", required=True, help="Yayın tarihi (örn: 23 Ağustos 2026)")
    parser.add_argument("--read_time", default="5 dk", help="Tahmini okuma süresi")
    parser.add_argument("--category", default="Edebiyat & Felsefe", help="Kategori")
    parser.add_argument("--content", required=True, help="Yazının tam metni (paragraflar çift satır boşluğu ile ayrılmalı)")
    parser.add_argument("--quote", default="", help="Vurgulanacak alıntı cümlesi")
    parser.add_argument("--tags", default="#Edebiyat,#Felsefe,#KaosunMimarıİnsan", help="Virgülle ayrılmış etiketler")

    args = parser.parse_args()

    tags_list = [t.strip() for t in args.tags.split(",") if t.strip()]
    content_html = format_content(args.content, args.quote)

    # 1. İlk paragrafı liste için özet (snippet) olarak al
    first_paragraph = [p.strip() for p in args.content.split("\n\n") if p.strip()][0]

    # 2. yazi-[slug].html dosyasını oluştur
    new_article_page = generate_article_page(
        title=args.title,
        slug=args.slug,
        date_str=args.date,
        read_time=args.read_time,
        category=args.category,
        content_html=content_html,
        tags=tags_list
    )
    
    article_filename = f"yazi-{args.slug}.html"
    with open(article_filename, "w", encoding="utf-8") as f:
        f.write(new_article_page)
    print(f"'{article_filename}' oluşturuldu.")

    # 3. kose-yazilari.html dosyasını güncelle
    update_kose_yazilari_list(
        title=args.title,
        slug=args.slug,
        date_str=args.date,
        read_time=args.read_time,
        category=args.category,
        snippet=first_paragraph
    )

if __name__ == "__main__":
    main()