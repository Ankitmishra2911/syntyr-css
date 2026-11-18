import { fail } from '@sveltejs/kit';
import { validateAccountName } from '../../lib/validation.js';

// Deliberately side-effect free. Production endpoints must authorize, apply
// CSRF protections, persist data, and handle concurrent writes.
export const actions = {
  default: async ({ request }) => {
    const body = await request.formData();
    const { value, error } = validateAccountName(body.get('name'));
    if (error) {
      return fail(400, { value, errors: { name: error } });
    }
    return { success: true, value };
  }
};
