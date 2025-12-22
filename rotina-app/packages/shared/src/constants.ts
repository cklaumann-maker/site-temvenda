export const MEAL_TYPES: Record<string, string> = {
  cafe: 'Café da Manhã',
  lanche_manha: 'Lanche da Manhã',
  almoco: 'Almoço',
  lanche_tarde: 'Lanche da Tarde',
  jantar: 'Jantar',
  ceia: 'Ceia',
};

export const DAYS_OF_WEEK: Record<number, string> = {
  1: 'Segunda-feira',
  2: 'Terça-feira',
  3: 'Quarta-feira',
  4: 'Quinta-feira',
  5: 'Sexta-feira',
  6: 'Sábado',
  7: 'Domingo',
};

export const DEFAULT_TIMEZONE = 'America/Sao_Paulo';

export const DEFAULT_MEALS_PER_DAY = 6;

export const EXPORT_CSV_HEADERS = {
  PLAN_TEMPLATE: [
    'org_name',
    'program_name',
    'week_index',
    'day_of_week',
    'day_label',
    'meal_type',
    'opt1',
    'opt2',
    'opt3',
    'avoid',
  ],
  USER_SCHEDULE: [
    'date',
    'day_label',
    'meal_type',
    'option_selected',
    'opt1',
    'opt2',
    'opt3',
    'avoid',
  ],
  ADHERENCE: [
    'date',
    'adherence_pct',
    'meals_done',
    'meals_planned',
    'weight_kg',
    'cardio_min',
    'workout_done',
    'functional',
  ],
};

