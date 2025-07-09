import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Plus, ChevronLeft } from "lucide-react";

// Définition d'un type pour les intervenants, pour un code plus propre et sûr
type Speaker = {
  id: number;
  name: string;
  role: string;
};

// Le composant est maintenant une page de formulaire complète et autonome.
const AddEventPage: React.FC = () => {
  const navigate = useNavigate();

  // --- GESTION DES DONNÉES DU FORMULAIRE (ÉTATS) ---
  // Chaque champ du formulaire a son propre état pour être contrôlé par React.
  const [eventName, setEventName] = useState("");
  const [eventLocation, setEventLocation] = useState("");
  const [eventDate, setEventDate] = useState("");
  const [startTime, setStartTime] = useState("");
  const [endTime, setEndTime] = useState("");
  const [isRecurring, setIsRecurring] = useState(false);
  const [frequency, setFrequency] = useState("");

  // États pour la section "Intervenant"
  const [selectedSpeaker, setSelectedSpeaker] = useState("");
  const [selectedRole, setSelectedRole] = useState("");
  const [addedSpeakers, setAddedSpeakers] = useState<Speaker[]>([]);
  const [nextSpeakerId, setNextSpeakerId] = useState(1);

  // --- GESTIONNAIRES D'ÉVÉNEMENTS ---

  // Logique pour le bouton "+" qui ajoute un intervenant au tableau
  const handleAddSpeaker = () => {
    if (!selectedSpeaker || !selectedRole) {
      alert(
        "Veuillez sélectionner un intervenant et un rôle avant de l'ajouter."
      );
      return;
    }
    const newSpeaker: Speaker = {
      id: nextSpeakerId,
      name: selectedSpeaker,
      role: selectedRole,
    };
    setAddedSpeakers([...addedSpeakers, newSpeaker]);
    setNextSpeakerId(nextSpeakerId + 1);
    setSelectedSpeaker("");
    setSelectedRole("");
  };

  // Gère la soumission du formulaire principal
  const handleSaveEvent = (e: React.FormEvent) => {
    e.preventDefault();

    const eventData = {
      name: eventName,
      location: eventLocation,
      date: eventDate,
      time: { start: startTime, end: endTime },
      recurring: { is: isRecurring, frequency: isRecurring ? frequency : null },
      speakers: addedSpeakers,
    };

    console.log("Données de l'événement à enregistrer :", eventData);
    alert("Événement enregistré ! (Vérifiez la console pour voir les données)");
    navigate("/events");
  };

  // Gère le clic sur le bouton "Annuler"
  const handleCancel = () => {
    navigate("/events");
  };

  // --- JSX (STRUCTURE VISUELLE DE LA PAGE) ---
  return (
    <div className="min-h-screen bg-gray-100 py-8 px-4 flex items-center justify-center">
      <div className="bg-white rounded-xl shadow-lg w-full max-w-3xl">
        <div className="p-8">
          <div className="mb-8">
            <h3 className="text-2xl font-bold text-gray-900">
              Ajout d'évènement
            </h3>
          </div>

          <form onSubmit={handleSaveEvent} className="space-y-8">
            {/* Nom et lieu de l'événement */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label
                  htmlFor="event-name"
                  className="block text-sm font-medium text-gray-700 mb-2"
                >
                  Nom de l'événement
                </label>
                <input
                  id="event-name"
                  type="text"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent transition"
                  placeholder="Nom événement"
                  value={eventName}
                  onChange={(e) => setEventName(e.target.value)}
                  required
                />
              </div>
              <div>
                <label
                  htmlFor="event-location"
                  className="block text-sm font-medium text-gray-700 mb-2"
                >
                  Lieu de l'événement
                </label>
                <input
                  id="event-location"
                  type="text"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent transition"
                  placeholder="Lieu événement"
                  value={eventLocation}
                  onChange={(e) => setEventLocation(e.target.value)}
                />
              </div>
            </div>

            {/* Date et heures */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div>
                <label
                  htmlFor="event-date"
                  className="block text-sm font-medium text-gray-700 mb-2"
                >
                  Date de l'événement
                </label>
                <input
                  id="event-date"
                  type="date"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent transition"
                  value={eventDate}
                  onChange={(e) => setEventDate(e.target.value)}
                  required
                />
              </div>
              <div>
                <label
                  htmlFor="start-time"
                  className="block text-sm font-medium text-gray-700 mb-2"
                >
                  Heure de début
                </label>
                <input
                  id="start-time"
                  type="time"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent transition"
                  value={startTime}
                  onChange={(e) => setStartTime(e.target.value)}
                  required
                />
              </div>
              <div>
                <label
                  htmlFor="end-time"
                  className="block text-sm font-medium text-gray-700 mb-2"
                >
                  Heure de fin
                </label>
                <input
                  id="end-time"
                  type="time"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent transition"
                  value={endTime}
                  onChange={(e) => setEndTime(e.target.value)}
                />
              </div>
            </div>

            {/* Récurrence */}
            <div className="flex items-center space-x-3">
              <input
                type="checkbox"
                id="recurring"
                className="h-4 w-4 text-green-600 focus:ring-green-500 border-gray-300 rounded"
                checked={isRecurring}
                onChange={(e) => setIsRecurring(e.target.checked)}
              />
              <label htmlFor="recurring" className="text-sm text-gray-700">
                Événement récurrent
              </label>
            </div>
            {isRecurring && (
              <div>
                <label
                  htmlFor="frequency"
                  className="block text-sm font-medium text-gray-700 mb-2"
                >
                  Fréquence de récurrence
                </label>
                <select
                  id="frequency"
                  className="w-full md:w-64 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent transition"
                  value={frequency}
                  onChange={(e) => setFrequency(e.target.value)}
                >
                  <option value="">Sélectionner une fréquence</option>
                  <option value="daily">Quotidien</option>
                  <option value="weekly">Hebdomadaire</option>
                  <option value="monthly">Mensuel</option>
                  <option value="yearly">Annuel</option>
                </select>
              </div>
            )}

            {/* Section Intervenant */}
            <div className="border-t pt-8">
              <div className="flex items-center justify-between mb-6">
                <h4 className="text-lg font-medium text-gray-900 uppercase">
                  Intervenant
                </h4>
                <button
                  type="button"
                  onClick={handleAddSpeaker}
                  className="w-10 h-10 border-2 border-dashed border-gray-300 rounded-full flex items-center justify-center hover:border-gray-400 transition-colors"
                  aria-label="Ajouter un intervenant"
                >
                  <Plus size={20} className="text-gray-600" />
                </button>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label
                    htmlFor="speaker"
                    className="block text-sm font-medium text-gray-700 mb-2"
                  >
                    Intervenant
                  </label>
                  <select
                    id="speaker"
                    value={selectedSpeaker}
                    onChange={(e) => setSelectedSpeaker(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent transition"
                  >
                    <option value="">Sélectionner un intervenant</option>
                    <option value="Jean Dupont">Jean Dupont</option>
                    <option value="Marie Curie">Marie Curie</option>
                    <option value="Louis Pasteur">Louis Pasteur</option>
                  </select>
                </div>
                <div>
                  <label
                    htmlFor="speaker-role"
                    className="block text-sm font-medium text-gray-700 mb-2"
                  >
                    Rôle intervenant
                  </label>
                  <select
                    id="speaker-role"
                    value={selectedRole}
                    onChange={(e) => setSelectedRole(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent transition"
                  >
                    <option value="">Sélectionner le rôle</option>
                    <option value="Conférencier">Conférencier</option>
                    <option value="Modérateur">Modérateur</option>
                    <option value="Organisateur">Organisateur</option>
                  </select>
                </div>
              </div>
              <div className="mt-6 border rounded-lg overflow-hidden">
                <table className="w-full text-sm">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-4 py-3 text-left font-medium text-gray-600">
                        Rôle
                      </th>
                      <th className="px-4 py-3 text-left font-medium text-gray-600">
                        Intervenant
                      </th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-200">
                    {addedSpeakers.length > 0 ? (
                      addedSpeakers.map((speaker) => (
                        <tr key={speaker.id}>
                          <td className="px-4 py-3 text-gray-800">
                            {speaker.role}
                          </td>
                          <td className="px-4 py-3 text-gray-800">
                            {speaker.name}
                          </td>
                        </tr>
                      ))
                    ) : (
                      <tr>
                        <td
                          colSpan={2}
                          className="px-4 py-6 text-center text-gray-500"
                        >
                          Aucun intervenant ajouté.
                        </td>
                      </tr>
                    )}
                  </tbody>
                </table>
              </div>
            </div>

            {/* Boutons d'action */}
            <div className="flex justify-end space-x-4 pt-8">
              <button
                type="button"
                onClick={handleCancel}
                className="px-6 py-2 text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors flex items-center gap-2"
              >
                <ChevronLeft size={16} /> Annuler
              </button>
              <button
                type="submit"
                className="px-6 py-2 text-white bg-green-600 rounded-lg hover:bg-green-700 transition-colors"
              >
                Enregistrer
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default AddEventPage;
