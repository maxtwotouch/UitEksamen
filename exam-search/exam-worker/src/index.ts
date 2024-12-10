import { createClient } from '@supabase/supabase-js'

export interface Env {
  SUPABASE_URL: string;
  SUPABASE_SERVICE_KEY: string;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    // Initialize Supabase Client for each request
    const supabase = createClient(env.SUPABASE_URL, env.SUPABASE_SERVICE_KEY)

    const url = new URL(request.url)
    
    // Simple routing:
    // GET /exams?course_code=XYZ
    if (url.pathname === '/exams' && request.method === 'GET') {
      const course_code = url.searchParams.get('course_code')
      let query = supabase.from('Exams').select('*')

      if (course_code) {
        query = query.ilike('course_code', `%${course_code}%`)
      }

      const { data, error } = await query

      if (error) {
        return new Response(JSON.stringify({ error: error.message }), {
          status: 500,
          headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' },
        })
      }

      return new Response(JSON.stringify(data || []), {
        status: 200,
        headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' },
      })
    }

    // Handle CORS preflight
    if (request.method === 'OPTIONS') {
      return new Response(null, {
        status: 204,
        headers: {
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'GET,OPTIONS',
          'Access-Control-Allow-Headers': 'Content-Type',
        },
      })
    }

    // Default 404 response
    return new Response(JSON.stringify({ message: 'Not Found' }), {
      status: 404,
      headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' },
    })
  },
}
