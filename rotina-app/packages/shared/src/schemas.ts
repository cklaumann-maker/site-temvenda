import { z } from 'zod';

export const dailyCheckinSchema = z.object({
  weight: z.number().min(0).max(500).optional(),
  workout_done: z.boolean(),
  workout_calories: z.number().int().min(0).max(2000).optional(),
  cardio_min: z.number().int().min(0).max(300).optional(),
  functional: z.boolean().optional().default(false),
});

export const markMealDoneSchema = z.object({
  meal_type: z.string(),
  option_selected: z.enum(['opt1', 'opt2', 'opt3']),
});

export const rulesetSchema = z.object({
  weekday_sweets_mode: z.enum(['HARD_BLOCK', 'EXCEPTION_WITH_COST', 'ALLOW']),
  hard_block_days: z.number().int().min(0).max(365),
  weekly_exception_limit: z.number().int().min(0).max(10),
  pizza_limit: z.number().int().min(0).max(10).optional(),
});

export const planTemplateSchema = z.object({
  program_id: z.string().uuid(),
  week_index: z.number().int().min(1),
  day_of_week: z.number().int().min(1).max(7),
  meal_type: z.enum(['cafe', 'lanche_manha', 'almoco', 'lanche_tarde', 'jantar', 'ceia']),
  opt1: z.string().nullable(),
  opt2: z.string().nullable(),
  opt3: z.string().nullable(),
  avoid: z.string().nullable(),
});

export const enrollmentSchema = z.object({
  user_id: z.string().uuid(),
  program_id: z.string().uuid(),
  start_date: z.string().date(),
});

export const exportDateRangeSchema = z.object({
  start_date: z.string().date(),
  end_date: z.string().date(),
}).refine((data) => {
  const start = new Date(data.start_date);
  const end = new Date(data.end_date);
  return end >= start;
}, {
  message: "Data final deve ser maior ou igual à data inicial",
});

