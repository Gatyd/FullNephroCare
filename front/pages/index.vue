<template>
    <div class="min-h-screen bg-blue-50 font-roboto">
    
  
      <!-- Bannière principale -->
      <section class="bg-gradient-to-r from-blue-600 to-blue-400 text-white py-16">
        <div class="container mx-auto px-4 flex flex-col md:flex-row items-center">
          <div class="md:w-1/2 mb-8 md:mb-0">
            <h2 class="text-3xl font-bold mb-4 font-poppins">Bienvenue sur la plateforme NephroCare</h2>
            <p class="text-lg mb-6">Votre outil complet pour la gestion et le suivi des patients atteints de maladie rénale chronique.</p>
        </div>
          <div class="md:w-1/2 flex justify-end items-center">
            <!-- Emplacement pour une image/illustration -->
             <img src="/public/logo.png" alt="Illustration">
          </div>
        </div>
      </section>
  
      <!-- Section À propos -->
      <section class="py-12 bg-white">
        <div class="container mx-auto px-4">
          <h2 class="text-2xl font-bold mb-8 text-center text-blue-500 font-poppins">À propos de NephroCare</h2>
          <div class="grid md:grid-cols-2 gap-8">
            <div>
              <h3 class="text-xl font-semibold mb-3 text-blue-500">Notre mission</h3>
              <p class="text-gray-700 mb-4">
                NephroCare est une plateforme dédiée à l'amélioration de la prise en charge des patients atteints de maladie rénale chronique (MRC). Notre mission est de fournir aux professionnels de santé des outils innovants pour un suivi optimal des patients.
              </p>
              <p class="text-gray-700">
                Grâce à notre plateforme, les médecins peuvent enregistrer, suivre et analyser les données des patients de manière sécurisée, facilitant ainsi la prise de décision médicale et améliorant la qualité des soins.
              </p>
            </div>
            <div>
              <h3 class="text-xl font-semibold mb-3 text-blue-500">L'enjeu de la MRC</h3>
              <p class="text-gray-700 mb-4">
                La maladie rénale chronique touche de nombreuses personnes à travers le monde et représente un enjeu majeur de santé publique. Un suivi rigoureux est essentiel pour ralentir sa progression et améliorer la qualité de vie des patients.
              </p>
              <p class="text-gray-700">
                Notre plateforme s'inscrit dans le cadre du projet AI4CKD qui vise à utiliser l'intelligence artificielle pour approfondir les recherches et améliorer la prise en charge des maladies rénales chroniques.
              </p>
            </div>
          </div>
        </div>
      </section>
  
      <!-- Section Fonctionnalités -->
      <section class="py-12 bg-blue-50">
        <div class="container mx-auto px-4">
          <h2 class="text-2xl font-bold mb-8 text-center text-blue-600 font-poppins">Nos fonctionnalités</h2>
          <div class="grid md:grid-cols-3 gap-6">
            <UCard class="bg-white shadow-md hover:shadow-lg transition-shadow">
              <template #header>
                <div class="flex justify-center p-4 bg-blue-100 rounded-t">
                  <div class="w-16 h-16 rounded-full bg-blue-500 flex items-center justify-center">
                    <span class="text-white text-2xl">📋</span>
                  </div>
                </div>
              </template>
              <div class="p-4 text-center">
                <h3 class="text-lg font-semibold mb-2 text-blue-500">Gestion des patients</h3>
                <p class="text-gray-600">Enregistrez et gérez les dossiers patients avec un accès facile à leurs informations médicales et administratives.</p>
              </div>
            </UCard>
  
            <UCard class="bg-white shadow-md hover:shadow-lg transition-shadow">
              <template #header>
                <div class="flex justify-center p-4 bg-blue-100 rounded-t">
                  <div class="w-16 h-16 rounded-full bg-blue-500 flex items-center justify-center">
                    <span class="text-white text-2xl">📊</span>
                  </div>
                </div>
              </template>
              <div class="p-4 text-center">
                <h3 class="text-lg font-semibold mb-2 text-blue-500">Suivi personnalisé</h3>
                <p class="text-gray-600">Créez des workflows de suivi sur mesure adaptés à chaque stade de la maladie rénale chronique.</p>
              </div>
            </UCard>
  
            <UCard class="bg-white shadow-md hover:shadow-lg transition-shadow">
              <template #header>
                <div class="flex justify-center p-4 bg-blue-100 rounded-t">
                  <div class="w-16 h-16 rounded-full bg-blue-500 flex items-center justify-center">
                    <span class="text-white text-2xl">🔔</span>
                  </div>
                </div>
              </template>
              <div class="p-4 text-center">
                <h3 class="text-lg font-semibold mb-2 text-blue-500">Alertes intelligentes</h3>
                <p class="text-gray-600">Recevez des notifications pour les changements d'état des patients et les résultats critiques d'examens.</p>
              </div>
            </UCard>
          </div>
        </div>
      </section>
  
      <!-- Section Statistiques -->
      <section class="py-12 bg-white">
        <div class="container mx-auto px-4">
          <h2 class="text-2xl font-bold mb-8 text-center text-blue-600 font-poppins">Impact de NephroCare</h2>
          <div class="grid grid-cols-2 md:grid-cols-4 gap-6 text-center">
            <div class="p-6 bg-blue-50 rounded-lg">
              <div class="text-3xl font-bold text-blue-600 mb-2">98%</div>
              <p class="text-gray-600">Satisfaction des professionnels de santé</p>
            </div>
            <div class="p-6 bg-blue-50 rounded-lg">
              <div class="text-3xl font-bold text-blue-600 mb-2">+500</div>
              <p class="text-gray-600">Patients suivis</p>
            </div>
            <div class="p-6 bg-blue-50 rounded-lg">
              <div class="text-3xl font-bold text-blue-600 mb-2">-25%</div>
              <p class="text-gray-600">Temps administratif</p>
            </div>
            <div class="p-6 bg-blue-50 rounded-lg">
              <div class="text-3xl font-bold text-blue-600 mb-2">+40%</div>
              <p class="text-gray-600">Efficacité du suivi</p>
            </div>
          </div>
        </div>
      </section>
  
      <!-- Section Témoignages -->
      <section class="py-12 bg-blue-50">
        <div class="container mx-auto px-4">
          <h2 class="text-2xl font-bold mb-8 text-center text-blue-600 font-poppins">Témoignages</h2>
          <UCarousel
            v-slot="{ item }"
            :items="testimonials"
            loop
            :autoplay="{ delay: 2000 }"
            :ui="{ 
              container: 'flex gap-4',
              item: 'basis-full md:basis-1/3 shrink-0 grow-0',
              dots: 'mt-4 md:mt-6'
            }"
          >
            <div class="bg-white rounded-lg shadow-lg p-6">
              <p class="italic text-gray-700 mb-4">"{{ item.quote }}"</p>
              <div class="flex items-center">
                <div class="w-12 h-12 rounded-full bg-blue-200 flex items-center justify-center mr-4">
                  <span class="text-blue-600 font-bold">{{ item.initials }}</span>
                </div>
                <div>
                  <h4 class="font-semibold">{{ item.name }}</h4>
                  <p class="text-sm text-gray-600">{{ item.role }}</p>
                </div>
              </div>
            </div>
          </UCarousel>
        </div>
      </section>
  
      <!-- Section CTA -->
      <section class="py-12 bg-blue-500 text-white">
        <div class="container mx-auto px-4 text-center">
          <h2 class="text-2xl font-bold mb-4 font-poppins">Prêt à améliorer le suivi de vos patients ?</h2>
          <p class="text-lg mb-6 max-w-2xl mx-auto">Découvrez comment NephroCare peut transformer votre pratique médicale et améliorer la qualité de vie de vos patients atteints de MRC.</p>
        </div>
      </section>
  
      <!-- Footer -->
      <footer class="bg-gray-800 text-white py-8">
        <div class="container mx-auto px-4">
          <div class="grid md:grid-cols-4 gap-8">
            <div>
              <h3 class="text-lg font-semibold mb-4">NephroCare</h3>
              <p class="text-gray-400">Une solution développée dans le cadre du projet AI4CKD pour améliorer la prise en charge des patients atteints de maladie rénale chronique.</p>
            </div>
            <div>
              <h3 class="text-lg font-semibold mb-4">Liens rapides</h3>
              <ul class="space-y-2 text-gray-400">
                <li><a href="#" class="hover:text-blue-300">Accueil</a></li>
                <li><a href="/home/patients" class="hover:text-blue-300">Patients</a></li>
                <li><a href="/home/consultations" class="hover:text-blue-300">Consultations</a></li>
                <li><a href="/home/settings" class="hover:text-blue-300">Paramètres</a></li>
              </ul>
            </div>
            <div>
              <h3 class="text-lg font-semibold mb-4">Ressources</h3>
              <ul class="space-y-2 text-gray-400">
                <li><a href="#" class="hover:text-blue-300">Guide d'utilisation</a></li>
                <li><a href="#" class="hover:text-blue-300">FAQ</a></li>
                <li><a href="#" class="hover:text-blue-300">Support technique</a></li>
                <li><a href="#" class="hover:text-blue-300">Formations</a></li>
              </ul>
            </div>
            <div>
              <h3 class="text-lg font-semibold mb-4">Contact</h3>
              <ul class="space-y-2 text-gray-400">
                <li>contact@nephrocare.org</li>
                <li>+229 XX XX XX XX</li>
                <li>IFRI-UAC, Abomey-Calavi, Bénin</li>
              </ul>
            </div>
          </div>
          <div class="mt-8 pt-6 border-t border-gray-700 text-center text-gray-400">
            <p>&copy; 2025 NephroCare - Projet AI4CKD. Tous droits réservés.</p>
          </div>
        </div>
      </footer>
    </div>
  </template>
  
  <script setup lang="ts">
  definePageMeta({
    layout: false,
  });
  
  const testimonials = [
    {
      quote: "Cette plateforme a révolutionné ma façon de suivre mes patients atteints de MRC.",
      name: "Dr. Roland Dupont",
      role: "Néphrologue, CHU de Cotonou",
      initials: "DR"
    },
    {
      quote: "L'automatisation des tâches administratives m'a permis de gagner un temps précieux.",
      name: "Sonia Kouassi",
      role: "Infirmière spécialisée",
      initials: "SK"
    },
    {
      quote: "Un outil indispensable pour une prise en charge optimale des patients.",
      name: "Dr. Aminata Diallo",
      role: "Néphrologue",
      initials: "AD"
    },
    {
      quote: "Interface intuitive et données fiables, que demander de plus ?",
      name: "Marc Benoît",
      role: "Infirmier coordinateur",
      initials: "MB"
    },
    {
      quote: "Une révolution dans le suivi des patients atteints de MRC.",
      name: "Dr. Sarah Martin",
      role: "Néphrologue",
      initials: "SM"
    },
    {
      quote: "La collaboration entre services n'a jamais été aussi simple.",
      name: "Paul Durant",
      role: "Coordinateur médical",
      initials: "PD"
    }
  ];
  </script>