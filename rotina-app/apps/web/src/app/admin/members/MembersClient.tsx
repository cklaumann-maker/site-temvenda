'use client';

import Link from 'next/link';

interface Member {
  id: string;
  user_id: string;
  role: string;
  profiles: {
    id: string;
    email: string | null;
    full_name: string | null;
  } | null;
}

interface MembersClientProps {
  members: Member[];
}

export default function MembersClient({ members }: MembersClientProps) {
  return (
    <div className="min-h-screen bg-gray-900 p-4">
      <div className="max-w-6xl mx-auto">
        <header className="mb-6">
          <h1 className="text-2xl font-bold text-white">Membros</h1>
        </header>

        <div className="space-y-4">
          {members.map((member) => (
            <Link
              key={member.id}
              href={`/admin/members/${member.user_id}`}
              className="block bg-gray-800 rounded-lg p-4 hover:bg-gray-700"
            >
              <div className="flex justify-between items-center">
                <div>
                  <h3 className="text-lg font-medium text-white">
                    {member.profiles?.full_name || member.profiles?.email || 'Sem nome'}
                  </h3>
                  <p className="text-sm text-gray-400">{member.profiles?.email}</p>
                </div>
                <div className="text-blue-400">→</div>
              </div>
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
}

