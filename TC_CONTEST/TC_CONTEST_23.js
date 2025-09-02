import { Selector } from 'testcafe';
const { BASE_URL } = require('../store');

fixture`Demo Login Test`
    .page`${BASE_URL}/accounts/login/`;

test('User can log in with valid credentials', async t => {
    const contestButton = Selector('a.nav-contest');
    const successMessage = Selector('option').withText('français (fr)');
    const languageSelect = Selector('select[name="language"]');

    await t
        .expect(contestButton.exists).ok('Contests button should be visible after login')
        .click(contestButton)
        .click(languageSelect)
        .click(languageSelect.find('option').withAttribute('value', 'fr'))
        .expect(successMessage.exists).ok('Should show French language option as selected');
});
