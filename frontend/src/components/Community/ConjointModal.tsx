import React, { useEffect, useRef, useState } from "react";
import { X } from "lucide-react";

type ConjointModalProps = {
  onClose: () => void;
  onSave: (selectedId: string) => void;
  members: { id: string; name: string; email?: string }[];
};

const ConjointModal: React.FC<ConjointModalProps> = ({
  onClose,
  onSave,
  members,
}) => {
  const [selectedId, setSelectedId] = useState("");
  const [error, setError] = useState("");
  const selectRef = useRef<HTMLSelectElement>(null);

  // Focus automatique sur le select à l'ouverture
  useEffect(() => {
    selectRef.current?.focus();
    const handleEsc = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };
    window.addEventListener("keydown", handleEsc);
    return () => window.removeEventListener("keydown", handleEsc);
  }, [onClose]);

  const handleSave = () => {
    if (!selectedId) {
      setError("Veuillez sélectionner un(e) conjoint(e).");
      return;
    }
    setError("");
    onSave(selectedId);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/30">
      <div className="bg-white rounded-md w-full max-w-xl p-6 relative shadow-lg">
        <button
          className="absolute top-3 right-3 text-gray-500 hover:text-red-600"
          onClick={onClose}
          aria-label="Fermer"
        >
          <X size={20} />
        </button>
        <h2 className="text-lg font-semibold mb-2 uppercase">
          Sélectionner un(e) conjoint(e)
        </h2>
        <p className="text-gray-500 mb-4 text-sm">
          Choisissez le membre à associer comme conjoint(e) à ce profil.
        </p>

        <label htmlFor="conjoint-select" className="block mb-2 font-medium">
          Liste des membres
        </label>
        <select
          id="conjoint-select"
          ref={selectRef}
          className="w-full p-3 border rounded-md focus:ring-2 focus:ring-green-500"
          value={selectedId}
          onChange={(e) => {
            setSelectedId(e.target.value);
            setError("");
          }}
        >
          <option value="">-- Sélectionnez un(e) conjoint(e) --</option>
          {members.map((m) => (
            <option key={m.id} value={m.id}>
              {m.name}
              {m.email ? ` (${m.email})` : ""}
            </option>
          ))}
        </select>
        {error && <div className="text-red-600 mt-2 text-sm">{error}</div>}

        <div className="mt-6 flex justify-end gap-4">
          <button
            onClick={onClose}
            className="px-4 py-2 bg-gray-200 text-gray-700 rounded hover:bg-gray-300"
            type="button"
          >
            Annuler
          </button>
          <button
            onClick={handleSave}
            className={`px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700 transition-colors ${
              !selectedId ? "opacity-50 cursor-not-allowed" : ""
            }`}
            disabled={!selectedId}
            type="button"
          >
            Enregistrer
          </button>
        </div>
      </div>
    </div>
  );
};

export default ConjointModal;
