import { useState, useMemo } from "react";
import { Link } from "react-router-dom";
import { Calendar, ChevronLeft, ChevronRight, X } from "lucide-react";

// --- COMPOSANT CALENDRIER DYNAMIQUE ---
const CalendarWidget = () => {
  const [currentDate, setCurrentDate] = useState(new Date(2020, 9, 1));
  const [selectedDate, setSelectedDate] = useState(new Date(2020, 9, 18));
  const handlePrevMonth = () =>
    setCurrentDate(
      (prev) => new Date(prev.getFullYear(), prev.getMonth() - 1, 1)
    );
  const handleNextMonth = () =>
    setCurrentDate(
      (prev) => new Date(prev.getFullYear(), prev.getMonth() + 1, 1)
    );

  const renderCalendarDays = () => {
    const year = currentDate.getFullYear();
    const month = currentDate.getMonth();
    const firstDayOfMonth = new Date(year, month, 1).getDay();
    const daysInMonth = new Date(year, month + 1, 0).getDate();
    const startDayIndex = firstDayOfMonth === 0 ? 6 : firstDayOfMonth - 1;
    const days = [];

    // Cellules vides pour les jours avant le début du mois
    for (let i = 0; i < startDayIndex; i++) {
      days.push(<div key={`empty-prev-${i}`}></div>);
    }

    // Jours du mois
    for (let day = 1; day <= daysInMonth; day++) {
      const isSelected =
        selectedDate.getDate() === day &&
        selectedDate.getMonth() === month &&
        selectedDate.getFullYear() === year;
      days.push(
        <div
          key={day}
          onClick={() => setSelectedDate(new Date(year, month, day))}
          className={`text-sm py-1.5 cursor-pointer rounded-full transition-colors flex items-center justify-center ${
            isSelected
              ? "bg-[#76C12C] text-white hover:bg-[#66a825]"
              : "text-gray-700 hover:bg-gray-100"
          }`}
        >
          {day}
        </div>
      );
    }
    return days;
  };

  return (
    <div className="bg-white rounded-lg shadow-sm p-4">
      <div className="flex items-center justify-between mb-4">
        <h3 className="font-semibold text-gray-800 capitalize">
          {currentDate.toLocaleString("fr-FR", {
            month: "long",
            year: "numeric",
          })}
        </h3>
        <div className="flex space-x-1">
          <button
            onClick={handlePrevMonth}
            className="p-1 hover:bg-gray-100 rounded-full text-gray-500"
          >
            <ChevronLeft size={18} />
          </button>
          <button
            onClick={handleNextMonth}
            className="p-1 hover:bg-gray-100 rounded-full text-gray-500"
          >
            <ChevronRight size={18} />
          </button>
        </div>
      </div>
      <div className="grid grid-cols-7 gap-y-2 text-center text-xs">
        {["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"].map((day) => (
          <div key={day} className="font-semibold text-gray-400 py-1">
            {day}
          </div>
        ))}
        {renderCalendarDays()}
      </div>
    </div>
  );
};
// --- COMPOSANT POUR AFFICHER UNE CARTE D'ÉVÉNEMENT ---
const EventCard = ({ event }: { event: any }) => (
  <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
    <div className="grid grid-cols-3 gap-4 items-center">
      <div>
        <p className="text-sm font-semibold text-gray-800">{event.title}</p>
        <p className="text-xs text-gray-500">
          {new Date(event.date).toLocaleDateString("fr-FR")}
        </p>
        <p className="text-xs text-gray-500">{event.time}</p>
      </div>
      <div>
        <p className="text-sm font-semibold text-gray-800">Intervenant</p>
        <p className="text-xs text-gray-500">{event.speaker}</p>
        <p className="text-xs text-gray-500">{event.location}</p>
      </div>
      <div>
        <p className="text-sm font-semibold text-gray-800">Rôle Intervenant</p>
        <p className="text-xs text-gray-500">{event.speakerRole}</p>
      </div>
    </div>
  </div>
);

// --- COMPOSANT PRINCIPAL DE LA PAGE ÉVÉNEMENTS ---
const EventsList = () => {
  const [activeTab, setActiveTab] = useState("current");
  const [dateFrom, setDateFrom] = useState("06/07/2025");
  const [dateTo, setDateTo] = useState("06/07/2025");
  const [showAddModal, setShowAddModal] = useState(false);

  // Données de simulation pour les événements
  const ALL_EVENTS = useMemo(
    () => [
      {
        id: 1,
        title: "Réunion de projet",
        date: new Date().toISOString().split("T")[0],
        time: "10:00",
        speaker: "Jean Dupont",
        speakerRole: "Chef de projet",
        location: "Salle A",
      },
      {
        id: 2,
        title: "Atelier Design",
        date: new Date().toISOString().split("T")[0],
        time: "14:00",
        speaker: "Marie Curie",
        speakerRole: "Lead Designer",
        location: "En ligne",
      },
      {
        id: 3,
        title: "Daily Standup (Passé)",
        date: new Date(new Date().setDate(new Date().getDate() - 1))
          .toISOString()
          .split("T")[0],
        time: "09:00",
        speaker: "Équipe Tech",
        speakerRole: "Développeurs",
        location: "Bureau 1",
      },
      {
        id: 4,
        title: "Présentation client (À venir)",
        date: new Date(new Date().setDate(new Date().getDate() + 2))
          .toISOString()
          .split("T")[0],
        time: "11:00",
        speaker: "Sophie Martin",
        speakerRole: "Commerciale",
        location: "Client Inc.",
      },
      {
        id: 5,
        title: "Planification Sprint (À venir)",
        date: new Date(new Date().setDate(new Date().getDate() + 5))
          .toISOString()
          .split("T")[0],
        time: "15:00",
        speaker: "Paul Robert",
        speakerRole: "Product Owner",
        location: "Salle B",
      },
    ],
    []
  );

  // Logique de filtrage des événements en fonction de l'onglet actif
  const filteredEvents = useMemo(() => {
    const today = new Date();
    today.setHours(0, 0, 0, 0); // Ignorer l'heure pour la comparaison de jours

    switch (activeTab) {
      case "previous":
        return ALL_EVENTS.filter((event) => new Date(event.date) < today);
      case "current":
        return ALL_EVENTS.filter(
          (event) =>
            new Date(event.date).toDateString() === today.toDateString()
        );
      case "upcoming":
        return ALL_EVENTS.filter((event) => new Date(event.date) > today);
      default:
        return [];
    }
  }, [activeTab, ALL_EVENTS]);

  return (
    <div className="min-h-screen bg-[#F8F9FA] p-4  sm:p-6 lg:p-8 font-sans">
      <div className="flex flex-col lg:flex-row gap-6 ">
        {/* COLONNE GAUCHE - CONTENU PRINCIPAL */}
        <div className="flex-1 ">
          <div className="bg-[#76C12C] rounded-lg p-10 mb-8 shadow-lg  ">
            <div className="flex items-start gap-4 text-white ">
              <Calendar size={36} className="mt-1" />
              <div>
                <h2 className="text-xl font-bold">Filtrer les événements</h2>
                <p className="text-sm">par période</p>
              </div>
            </div>
            <div className="flex items-center space-x-4 mt-4">
              <div className="relative">
                <input
                  type="text"
                  value={dateFrom}
                  onChange={(e) => setDateFrom(e.target.value)}
                  className="pl-10 pr-3 py-2 bg-white rounded-md text-gray-900 w-40 focus:ring-2 focus:ring-white/50 focus:outline-none"
                />
                <Calendar
                  size={18}
                  className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400"
                />
              </div>
              <div className="relative">
                <input
                  type="text"
                  value={dateTo}
                  onChange={(e) => setDateTo(e.target.value)}
                  className="pl-10 pr-3 py-2 bg-white rounded-md text-gray-900 w-40 focus:ring-2 focus:ring-white/50 focus:outline-none"
                />
                <Calendar
                  size={18}
                  className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400"
                />
              </div>
              <button className="px-8 py-2 bg-gray-700 text-white font-semibold rounded-md hover:bg-gray-800 transition-colors border border-gray-500">
                Charger
              </button>
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-6 ">
            <div
              onClick={() => setActiveTab("previous")}
              className={` p-4 rounded-lg shadow-sm cursor-pointer transition-colors ${
                activeTab === "previous"
                  ? "bg-[#A6D785]"
                  : "bg-white hover:bg-gray-50"
              }`}
            >
              <h3 className="text-xs font-bold text-gray-600 uppercase">
                Événement Précédent
              </h3>
              <p className="text-sm text-gray-500 mt-1">Date heure</p>
            </div>
            <div
              onClick={() => setActiveTab("current")}
              className={`p-4 rounded-lg shadow-sm cursor-pointer transition-colors ${
                activeTab === "current"
                  ? "bg-[#A6D785]"
                  : "bg-white hover:bg-gray-50"
              }`}
            >
              <h3 className="text-xs font-bold text-gray-800 uppercase">
                Événement en Cours
              </h3>
              <p className="text-sm text-gray-700 mt-1">Date heure</p>
            </div>
            <div
              onClick={() => setActiveTab("upcoming")}
              className={`p-4 rounded-lg shadow-sm cursor-pointer transition-colors ${
                activeTab === "upcoming"
                  ? "bg-[#A6D785]"
                  : "bg-white hover:bg-gray-50"
              }`}
            >
              <h3 className="text-xs font-bold text-gray-600 uppercase">
                Événement à Venir
              </h3>
              <p className="text-sm text-gray-500 mt-1">Date heure</p>
            </div>
          </div>

          {/* SECTION DYNAMIQUE POUR LA LISTE DES ÉVÉNEMENTS */}
          <div className="space-y-4">
            {filteredEvents.length > 0 ? (
              filteredEvents.map((event) => (
                <EventCard key={event.id} event={event} />
              ))
            ) : (
              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-8 text-center text-gray-500">
                <p>Aucun événement trouvé pour cette période.</p>
              </div>
            )}
          </div>
        </div>

        {/* COLONNE DROITE - BARRE LATÉRALE */}
        <div className="w-full lg:w-72 flex-shrink-0">
          <div className="space-y-6">
            <Link
              to="/events/add" 
              className="block text-center w-full bg-[#76C12C] text-white py-2.5 rounded-lg hover:bg-[#66a825] transition-colors font-semibold shadow-md"
            >
              Ajouter un événement
            </Link>
            <CalendarWidget />
            <div className="bg-white rounded-lg shadow-sm">
              <div className="bg-[#76C12C] text-white text-center font-semibold py-2.5 rounded-t-lg">
                Filtrer par
              </div>
              <div className="p-4">
                <h4 className="text-sm font-bold text-gray-800 mb-3 uppercase">
                  STOPS
                </h4>
                <div className="space-y-3">
                  {["All Flights", "No Stops", "1 Stop", "2 Stops"].map(
                    (stop, index) => (
                      <label
                        key={stop}
                        className="flex items-center space-x-3 cursor-pointer"
                      >
                        <input
                          type="radio"
                          name="stops"
                          defaultChecked={index === 0}
                          className="h-5 w-5 rounded-full border-2 border-gray-300 text-[#76C12C] focus:ring-[#76C12C] appearance-none checked:bg-[#76C12C] checked:border-[#76C12C] transition-all"
                        />
                        <span className="text-sm text-gray-700">{stop}</span>
                      </label>
                    )
                  )}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default EventsList;
