<?php
/*
 Template Name: TEM VENDA — Landing
 Template Post Type: page
*/
?><!doctype html>
<html <?php language_attributes(); ?>>
<head>
<meta charset="<?php bloginfo('charset'); ?>" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title><?php bloginfo('name'); ?> | <?php the_title(); ?></title>

<!-- Fonte & Tailwind -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;800&display=swap" rel="stylesheet">
<script src="https://cdn.tailwindcss.com"></script>
<script>
  tailwind.config = {
    theme: {
      extend: {
        colors: { tvgreen:'#5ee100', tvgray:'#373736' },
        fontFamily: { sans: ['Montserrat','ui-sans-serif','system-ui'] },
      }
    }
  }
</script>

<?php wp_head(); ?>
<style>
  body{background:#000;color:#fff;font-family:Montserrat,system-ui,-apple-system,Segoe UI,Roboto,Arial}
</style>
</head>
<body <?php body_class('bg-black text-white antialiased'); ?>>

  <!-- NAVBAR -->
  <header class="sticky top-0 z-40 backdrop-blur bg-black/70 border-b border-white/10">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
      <div class="flex items-center gap-3">
        <div class="h-9 w-9 rounded-full bg-[#5ee100] grid place-items-center font-black text-black">TV</div>
        <span class="font-extrabold tracking-wide">TEM VENDA</span>
      </div>

      <nav class="hidden md:flex items-center gap-8 text-sm text-white/80">
        <a href="#solucoes" class="hover:text-white">Soluções</a>
        <a href="#prova" class="hover:text-white">Resultados</a>
        <a href="#sobre" class="hover:text-white">Sobre</a>
        <a href="#contato" class="hover:text-white">Contato</a>
      </nav>

      <div class="hidden md:flex gap-3">
        <a href="#diagnostico" class="inline-flex items-center gap-2 rounded-2xl px-4 py-2 bg-[#5ee100] text-black font-semibold shadow hover:translate-y-[-1px] transition">
          Agendar diagnóstico
        </a>
      </div>
    </div>
  </header>

  <!-- HERO -->
  <section class="relative overflow-hidden">
    <div class="absolute inset-0 opacity-30" style="background:radial-gradient(1200px 600px at 50% -10%, rgba(94,225,0,0.35), transparent)"></div>
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 md:py-28 grid md:grid-cols-2 gap-10 items-center">
      <div>
        <div class="inline-flex items-center gap-2 text-xs font-semibold text-black bg-[#5ee100] rounded-full px-3 py-1 mb-4">
          Comunidade de líderes em farmácia
        </div>
        <h1 class="text-4xl md:text-6xl font-extrabold leading-tight">
          De gestores comuns a <span class="text-[#5ee100]">líderes de alta performance</span>.
        </h1>
        <p class="mt-5 text-lg text-white/80 max-w-xl">
          Consultoria, mentoria, treinamentos e formação para você viver a melhor versão de gestor que sua farmácia já teve — com rituais práticos e indicadores que geram resultado.
        </p>
        <div class="mt-8 flex flex-col sm:flex-row gap-3">
          <a href="#formacao" class="inline-flex items-center justify-center gap-2 rounded-2xl px-5 py-3 bg-[#5ee100] text-black font-bold">
            Quero liderar meu time →
          </a>
          <a href="#whats" class="inline-flex items-center justify-center gap-2 rounded-2xl px-5 py-3 border border-white/20 hover:border-white/40">
            Chamar no Whats
          </a>
        </div>
        <div class="mt-8 flex flex-wrap items-center gap-6 text-sm text-white/60">
          <span>+300 gestores treinados</span>
          <span>NPS 9,6</span>
          <span>3 redes parceiras</span>
        </div>
      </div>

      <div class="relative">
        <div class="absolute -inset-1 rounded-3xl bg-gradient-to-br from-[#5ee100] to-transparent blur-2xl opacity-30"></div>
        <div class="relative bg-[#0b0b0b] border border-white/10 rounded-3xl p-6 md:p-10 shadow-2xl">
          <div class="text-sm text-white/60 mb-2">Plano de 90 dias</div>
          <ul class="space-y-3">
            <li class="flex gap-3"><span class="text-[#5ee100]">✔</span> Diagnóstico e metas</li>
            <li class="flex gap-3"><span class="text-[#5ee100]">✔</span> Roteiro de vendas no balcão</li>
            <li class="flex gap-3"><span class="text-[#5ee100]">✔</span> Rituais de 15’ e indicadores</li>
            <li class="flex gap-3"><span class="text-[#5ee100]">✔</span> Feedbacks e liderança na prática</li>
          </ul>
          <a id="diagnostico" href="#contato" class="mt-6 inline-block rounded-2xl px-4 py-2 bg-[#5ee100] text-black font-semibold">
            Agendar diagnóstico
          </a>
        </div>
      </div>
    </div>
  </section>

  <!-- PROBLEMA -->
  <section id="problema" class="py-16 md:py-24 border-t border-white/10 bg-[#0b0b0b]">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 grid md:grid-cols-2 gap-10 items-center">
      <div>
        <h2 class="text-3xl md:text-4xl font-extrabold">Meta apertada, equipe cansada e resultado oscilando?</h2>
        <p class="mt-4 text-white/70">Você não está sozinho. A maioria dos gestores luta com rotatividade, falta de rotina de indicadores e pouca disciplina no balcão.</p>
      </div>
      <ul class="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <li class="rounded-2xl border border-white/10 p-4 bg-black/40">Sem roteiro de vendas no atendimento</li>
        <li class="rounded-2xl border border-white/10 p-4 bg-black/40">Indicadores sem dono ou sem rotina</li>
        <li class="rounded-2xl border border-white/10 p-4 bg-black/40">Ticket médio e genéricos estagnados</li>
        <li class="rounded-2xl border border-white/10 p-4 bg-black/40">Falta de alinhamento e feedbacks</li>
      </ul>
    </div>
  </section>

  <!-- SOLUÇÕES -->
  <section id="solucoes" class="py-16 md:py-24">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <h2 class="text-3xl md:text-4xl font-extrabold mb-10">Como o TEM VENDA guia sua jornada</h2>
      <div class="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
        <a href="#formacao" class="group rounded-3xl border border-white/10 p-6 bg-[#0b0b0b] hover:border-[#5ee100]/60 transition">
          <div class="h-10 w-10 rounded-xl bg-[#5ee100] grid place-items-center font-extrabold text-black mb-4">1</div>
          <h3 class="font-bold text-lg">Formação Líder de Farmácia</h3>
          <p class="text-white/70 mt-1">Lidere pessoas, bata metas e engaje o time.</p>
        </a>
        <a href="#treinamento" class="group rounded-3xl border border-white/10 p-6 bg-[#0b0b0b] hover:border-[#5ee100]/60 transition">
          <div class="h-10 w-10 rounded-xl bg-[#5ee100] grid place-items-center font-extrabold text-black mb-4">2</div>
          <h3 class="font-bold text-lg">Treinamento In Company</h3>
          <p class="text-white/70 mt-1">Rotina e técnica no balcão, na prática.</p>
        </a>
        <a href="#consultoria" class="group rounded-3xl border border-white/10 p-6 bg-[#0b0b0b] hover:border-[#5ee100]/60 transition">
          <div class="h-10 w-10 rounded-xl bg-[#5ee100] grid place-items-center font-extrabold text-black mb-4">3</div>
          <h3 class="font-bold text-lg">Consultoria</h3>
          <p class="text-white/70 mt-1">Processo, estratégia e indicadores que funcionam.</p>
        </a>
        <a href="#palestras" class="group rounded-3xl border border-white/10 p-6 bg-[#0b0b0b] hover:border-[#5ee100]/60 transition">
          <div class="h-10 w-10 rounded-xl bg-[#5ee100] grid place-items-center font-extrabold text-black mb-4">4</div>
          <h3 class="font-bold text-lg">Palestras</h3>
          <p class="text-white/70 mt-1">Direção e energia para eventos e convenções.</p>
        </a>
      </div>
    </div>
  </section>

  <!-- SOBRE (opcional: adicione sua história/foto) -->
  <section id="sobre" class="py-16 md:py-24">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 grid md:grid-cols-2 gap-10 items-center">
      <div>
        <h2 class="text-3xl md:text-4xl font-extrabold">Quem guia a sua jornada</h2>
        <p class="mt-4 text-white/70">Cesar Klaumann — consultor e mentor em gestão comercial humanizada, especializado em farmácias. Metodologia prática, indicadores simples e rituais de liderança que cabem no dia a dia.</p>
      </div>
      <div class="relative">
        <div class="absolute -inset-1 rounded-3xl bg-gradient-to-br from-[#5ee100] to-transparent blur-2xl opacity-30"></div>
        <div class="relative aspect-[4/3] rounded-3xl border border-white/10 bg-[radial-gradient(circle_at_30%_30%,rgba(94,225,0,.15),transparent_60%),linear-gradient(180deg,#0b0b0b,#000)] grid place-items-center">
          <div class="text-center">
            <div class="text-6xl font-black text-white/10">LEÃO</div>
            <div class="mt-2 text-white/60">Identidade forte, foco em resultado</div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- FOOTER -->
  <footer id="contato" class="border-t border-white/10 bg-black">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 grid md:grid-cols-3 gap-8">
      <div>
        <div class="flex items-center gap-3">
          <div class="h-9 w-9 rounded-full bg-[#5ee100] grid place-items-center font-black text-black">TV</div>
          <span class="font-extrabold tracking-wide">TEM VENDA</span>
        </div>
        <p class="text-sm text-white/60 mt-3 max-w-sm">Ajudamos gestores a liderar pessoas e aumentar resultados com um método prático e mensurável.</p>
      </div>
      <div>
        <div class="font-bold mb-3">Soluções</div>
        <ul class="space-y-2 text-white/70 text-sm">
          <li><a href="#formacao" class="hover:text-white">Formação Líder de Farmácia</a></li>
          <li><a href="#treinamento" class="hover:text-white">Treinamento In Company</a></li>
          <li><a href="#consultoria" class="hover:text-white">Consultoria Empresarial</a></li>
          <li><a href="#palestras" class="hover:text-white">Palestras</a></li>
        </ul>
      </div>
      <div>
        <div class="font-bold mb-3">Contato</div>
        <ul class="space-y-2 text-white/70 text-sm">
          <li id="whats">WhatsApp: (48) 9 9999-9999</li>
          <li>E-mail: contato@temvenda.com.br</li>
          <li>Balneário Camboriú — SC</li>
        </ul>
        <a href="https://wa.me/5548999999999" class="mt-4 inline-block rounded-2xl px-4 py-2 bg-[#5ee100] text-black font-semibold">
          Chamar no Whats
        </a>
      </div>
    </div>
    <div class="py-5 border-t border-white/10 text-center text-xs text-white/50">© <?php echo date('Y'); ?> TEM VENDA — Todos os direitos reservados.</div>
  </footer>

<?php wp_footer(); ?>
</body>
</html>