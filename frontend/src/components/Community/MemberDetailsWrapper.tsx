import React from "react";
import { useParams, useNavigate } from "react-router-dom";
import MemberDetailsPage from "./MemberDetailsPage";
import { generateMockMembers } from "./MembersList";

const MemberDetailsWrapper = () => {
  const { id } = useParams();
  const navigate = useNavigate();

  const MOCK_MEMBERS = generateMockMembers(652); // Doit matcher ta logique de base
  const member = MOCK_MEMBERS.find((m) => m.id === id);

  if (!member) {
    return (
      <div className="p-8 text-center">
        <p className="text-lg text-gray-700">Membre non trouvé.</p>
        <button
          onClick={() => navigate(-1)}
          className="mt-4 text-blue-600 underline"
        >
          Retour
        </button>
      </div>
    );
  }

  return <MemberDetailsPage member={member} onBack={() => navigate(-1)} />;
};

export default MemberDetailsWrapper;
