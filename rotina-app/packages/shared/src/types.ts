export type UserRole = 'OWNER' | 'COACH' | 'MEMBER';

export type WeekdaySweetsMode = 'HARD_BLOCK' | 'EXCEPTION_WITH_COST' | 'ALLOW';

export type MealType = 
  | 'cafe' 
  | 'lanche_manha' 
  | 'almoco' 
  | 'lanche_tarde' 
  | 'jantar' 
  | 'ceia';

export type OptionSelected = 'opt1' | 'opt2' | 'opt3';

export type RuleEventType = 
  | 'SWEET_BLOCKED' 
  | 'SWEET_EXCEPTION_USED' 
  | 'PIZZA_CONSUMED' 
  | 'PIZZA_LIMIT_EXCEEDED';

export interface Profile {
  id: string;
  email: string | null;
  full_name: string | null;
  avatar_url: string | null;
  created_at: string;
  updated_at: string;
}

export interface Org {
  id: string;
  name: string;
  slug: string;
  created_at: string;
  updated_at: string;
}

export interface OrgMember {
  id: string;
  org_id: string;
  user_id: string;
  role: UserRole;
  active: boolean;
  created_at: string;
  updated_at: string;
}

export interface Program {
  id: string;
  org_id: string;
  name: string;
  description: string | null;
  active: boolean;
  created_at: string;
  updated_at: string;
}

export interface Enrollment {
  id: string;
  user_id: string;
  program_id: string;
  start_date: string;
  end_date: string | null;
  active: boolean;
  created_at: string;
  updated_at: string;
}

export interface Ruleset {
  id: string;
  program_id: string;
  weekday_sweets_mode: WeekdaySweetsMode;
  hard_block_days: number;
  weekly_exception_limit: number;
  pizza_limit: number | null;
  created_at: string;
  updated_at: string;
}

export interface PlanTemplate {
  id: string;
  program_id: string;
  week_index: number;
  day_of_week: number; // 1-7 (Monday-Sunday)
  meal_type: MealType;
  opt1: string | null;
  opt2: string | null;
  opt3: string | null;
  avoid: string | null;
  created_at: string;
  updated_at: string;
}

export interface DailyMeal {
  id: string;
  user_id: string;
  date: string;
  meal_type: MealType;
  opt1: string | null;
  opt2: string | null;
  opt3: string | null;
  avoid: string | null;
  option_selected: OptionSelected | null;
  kcal_opt1: number;
  kcal_opt2: number;
  kcal_opt3: number;
  kcal_other: number | null;
  other_description: string | null;
  created_at: string;
  updated_at: string;
}

export interface DailyCheckin {
  id: string;
  user_id: string;
  date: string;
  weight_kg: number | null;
  workout_done: boolean;
  cardio_min: number;
  functional: boolean;
  workout_calories: number;
  created_at: string;
  updated_at: string;
}

export interface RuleEvent {
  id: string;
  user_id: string;
  event_type: RuleEventType;
  date: string;
  description: string | null;
  metadata: Record<string, unknown> | null;
  created_at: string;
}

export interface SweetPermissionResult {
  allowed: boolean;
  requires_confirmation?: boolean;
  message: string;
}

export interface AdherenceData {
  date: string;
  adherence_pct: number;
  meals_done: number;
  meals_planned: number;
}

export interface UserProfile {
  user_id: string;
  name: string | null;
  phone: string | null;
  cpf: string | null;
  city: string | null;
  state: string | null;
  height_cm: number | null;
  weight_kg: number | null;
  max_daily_calories: number | null;
  created_at?: string;
  updated_at?: string;
}

