import { Selector } from 'testcafe';
//run in 2 terminal
const { BASE_URL } = require('../store');

fixture`Demo Login Test`
    .page`${BASE_URL}/accounts/login/`;

test('User can log in with valid credentials', async t => {
    const usernameInput = Selector('#id_username');
    const passwordInput = Selector('#id_password');
    const loginButton = Selector('button[type="submit"]');
    const contestButton = Selector('a.nav-contest');
    const successMessage = Selector('li.active-page a').withText('2');
    const page2Button = Selector('ul.pagination a').withAttribute('href', '/contests/?page=2#past-contests');

    await t
        .typeText(usernameInput, 'admin')
        .typeText(passwordInput, 'Ducanh12a1@!')
        .click(loginButton)
        .expect(contestButton.exists).ok('Contests button should be visible after login')
        .click(contestButton)
        .click(page2Button)
        .expect(successMessage.exists).ok('Should show contest banner after clicking contest link');

});
