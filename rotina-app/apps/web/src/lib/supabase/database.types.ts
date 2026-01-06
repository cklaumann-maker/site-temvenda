// Generated types for Supabase - placeholder
// Run: npx supabase gen types typescript --project-id <project-id> > src/lib/supabase/database.types.ts
export type Database = {
  public: {
    Tables: {
      profiles: {
        Row: {
          id: string;
          email: string | null;
          full_name: string | null;
          avatar_url: string | null;
          created_at: string;
          updated_at: string;
        };
        Insert: Omit<Database['public']['Tables']['profiles']['Row'], 'created_at' | 'updated_at'>;
        Update: Partial<Database['public']['Tables']['profiles']['Insert']>;
      };
      // Add other tables as needed
    };
  };
};







