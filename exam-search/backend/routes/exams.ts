import { Router, Request, Response } from 'express';
import { supabase } from '../lib/supabaseClient';

const router = Router();

router.get('/', async (req: Request, res: Response): Promise<void> => {
  try {
    const { course_code } = req.query;

    let query = supabase.from('Exams').select('*');

    if (course_code && typeof course_code === 'string') {
      query = query.ilike('course_code', `%${course_code}%`);
    }

    const { data, error } = await query;

    if (error) {
      res.status(500).json({ error: error.message });
      return;
    }

    if (!data || data.length === 0) {
      res.status(404).json({ message: 'No exams found' });
      return;
    }

    res.json(data);
  } catch (error) {
    res.status(500).json({ message: 'Internal Server Error' });
  }
});

export default router;
