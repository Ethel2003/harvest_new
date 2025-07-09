import React, { useEffect, useRef, useState } from "react";
import { X } from "lucide-react";

type ChildModalProps = {
  onClose: () => void;
  onSave: (selectedIds: string[]) => void;
  childrenList: { id: string; name: string }[];
};

const ChildModal: React.FC<ChildModalProps> = ({
  onClose,
  onSave,
  childrenList,
}) => {
  const [selected, setSelected] = useState<string[]>([]);
  const [error, setError] = useState("");
  const selectRef = useRef<HTMLSelectElement>(null);

  // Focus automatique sur le select et fermeture par Échap
  useEffect(() => {
    selectRef.current?.focus();
    const handleEsc = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };
    window.addEventListener("keydown", handleEsc);
    return () => window.removeEventListener("keydown", handleEsc);
  }, [onClose]);

  const handleChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const options = Array.from(e.target.selectedOptions);
    setSelected(options.map((opt) => opt.value));
    setError("");
  };

  const handleSave = () => {
    if (selected.length === 0) {
      setError("Veuillez sélectionner au moins un enfant.");
      return;
    }
    setError("");
    onSave(selected);
  };

  return (
    <div className="fixed inset-0 z-50 bg-black/40 flex items-center justify-center">
      <div className="bg-white rounded-md p-6 w-full max-w-lg relative shadow-lg">
        <button
          onClick={onClose}
          className="absolute top-3 right-3 text-gray-500 hover:text-red-600"
          aria-label="Fermer"
        >
          <X size={20} />
        </button>

        <h2 className="text-lg font-semibold uppercase mb-2">
          Sélectionner des enfants
        </h2>
        <p className="text-gray-500 mb-4 text-sm">
          Sélectionnez un ou plusieurs enfants à associer à ce membre.
        </p>

        <label htmlFor="children-select" className="block mb-2 font-medium">
          Liste des enfants
        </label>
        <select
          id="children-select"
          ref={selectRef}
          multiple
          size={Math.min(6, childrenList.length || 3)}
          className="w-full border rounded p-2 focus:ring-2 focus:ring-blue-500 cursor-pointer"
          value={selected}
          onChange={handleChange}
        >
          {childrenList.length === 0 ? (
            <option disabled>Aucun enfant disponible</option>
          ) : (
            childrenList.map((child) => (
              <option key={child.id} value={child.id}>
                {child.name}
              </option>
            ))
          )}
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
            className={`px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors font-medium shadow ${
              selected.length === 0 ? "opacity-50 cursor-not-allowed" : ""
            }`}
            disabled={selected.length === 0}
            type="button"
          >
            Enregistrer
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChildModal;
