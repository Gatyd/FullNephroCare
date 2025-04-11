export const useDefaultMedecins = () => {
  const defaultMedecins = [
    {
      id: 1,
      first_name: 'Pierre',
      last_name: 'Dubois',
      specialite: 'Néphrologie',
      email: 'pierre.dubois@nephrocare.fr'
    },
    {
      id: 2,
      first_name: 'Marie',
      last_name: 'Laurent',
      specialite: 'Néphrologie',
      email: 'marie.laurent@nephrocare.fr'
    },
    {
      id: 3,
      first_name: 'Antoine',
      last_name: 'Moreau',
      specialite: 'Néphrologie',
      email: 'antoine.moreau@nephrocare.fr'
    },
    {
      id: 4,
      first_name: 'Claire',
      last_name: 'Leroy',
      specialite: 'Néphrologie',
      email: 'claire.leroy@nephrocare.fr'
    }
  ]

  return {
    defaultMedecins
  }
}