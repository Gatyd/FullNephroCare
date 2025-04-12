export interface LoginResponse {
	success: boolean;
	message: string;
}

export interface User{
    id: number;
	first_name: string;
	last_name: string;
	email: string;
    is_staff: boolean;
}

export interface Patient{
    id: number;
    numero_dossier: string;
    nom: string;
    prenom: string;
    date_naissance: string;
    sexe: string;
    adresse: string;
    telephone: string;
    email: string;
    stade_mrc: number;
    dfu: number;
    antecedents_medicaux: string;
    allergies: string;
    medecin_referent: User;
    date_creation: string;
    date_modification: string;
}

export interface Consultation{
    id: number;
    patient: Patient;
    medecin: User;
    date: string;
    type_consultation: string;
    symptomes: string;
    diagnostic: string;
}

interface Prescription {
    id: number;
    consultation: number; // ID de la consultation (ForeignKey)
    medicament: string;
    posologie: string;
    duree_traitement: number; // en jours
    instructions?: string;
    est_convertie: boolean;
    date_conversion?: string | null; // DateTime
    date_creation: string; // DateTime
}

interface Examen {
    id: number;
    consultation: number | Consultation; // ID de la consultation (ForeignKey)
    type_examen: string;
    description?: string;
    date_realisation: string; // Date
    urgence: boolean;
    resultat?: number | null; // ID du résultat (OneToOneField)
    date_creation: string; // DateTime
}

interface Appointment {
    id: number;
    patient: number | Patient; // ID du patient (ForeignKey)
    medecin: number; // ID de l'utilisateur (ForeignKey)
    date_prevue: string; // DateTime
    motif: string;
    notes_preparation?: string;
    examen_prealable?: number | Examen | null; // ID de l'examen (ForeignKey)
    statut: 'PLANIFIE' | 'ANNULE' | 'COMPLETE';
}
interface AlerteCritere {
    id: number;
    patient: number; // ID du patient
    nom: string;
    description: string;
    type_alerte: 'DFU' | 'CREATININE' | 'EXAMEN';
    seuil_valeur?: number | null;
    actif: boolean;
    createur: number; // ID de l'utilisateur
    date_creation: string; // DateTime
}

interface UserNotification {
    id: number;
    titre: string;
    message: string;
    type_notification: 'ALERTE' | 'RENDEZ_VOUS';
    patient?: number | null; // ID du patient
    destinataire: number; // ID de l'utilisateur
    date_lecture?: string | null; // DateTime
    critere_alerte?: number | null; // ID de l'alerte critère
    date_creation: string; // DateTime
    date_expiration?: string | null; // DateTime
}

interface ReglageNotification {
    id: number;
    utilisateur: number; // ID de l'utilisateur (OneToOne)
    recevoir_alertes: boolean;
    recevoir_rdv: boolean;
    email_actif: boolean;
    date_modification: string; // DateTime
}

interface TraitementEnCours {
    id: number;
    patient: number; // ID du patient
    medicament: string;
    posologie: string;
    date_debut: string; // Date
    date_fin?: string | null; // Date
    prescripteur?: number | null; // ID de l'utilisateur
    commentaire?: string | null;
    prescription_origine?: number | null; // ID de la prescription
    est_actif: boolean;
    date_modification: string; // DateTime
    traitement_precedent?: number | null; // ID du traitement précédent (self reference)
}

interface ResultatExamen {
    id: number;
    patient: number; // ID du patient
    examen_prescrit?: number | null; // ID de l'examen
    type_examen: string;
    date_realisation: string; // Date
    laboratoire?: string;
    resultats_texte?: string;
    fichier_resultats?: string | null; // Chemin du fichier
    creatinine?: number | null;
    dfu?: number | null;
    proteinurie?: number | null;
    interpretation?: string;
    est_anormal: boolean;
    date_ajout: string; // DateTime
    ajoute_par?: number | null; // ID de l'utilisateur
}