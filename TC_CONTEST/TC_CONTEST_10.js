import { Selector } from 'testcafe';
const { BASE_URL } = require('../store');

fixture`Demo Login Test`
    .page`${BASE_URL}/accounts/login/`;

test('User can log in with valid credentials', async t => {
    const usernameInput = Selector('#id_username');
    const passwordInput = Selector('#id_password');
    const loginButton = Selector('button[type="submit"]');
    const contestButton = Selector('a.nav-contest');
    const calendarTab = Selector('a').withText('Calendar');
    const successMessage = Selector('h2').withText('Contests in');

    await t
        .typeText(usernameInput, 'admin')
        .typeText(passwordInput, 'Ducanh12a1@!')
        .click(loginButton)
        .expect(contestButton.exists).ok('Contests button should be visible after login')
        .click(contestButton)
        .expect(calendarTab.exists).ok('Calendar tab should be visible')
        .click(calendarTab)
        .expect(successMessage.exists).ok('Should show success message after login');
});
