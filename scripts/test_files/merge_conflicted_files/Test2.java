package works.buddy.samples ;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.io.PrintWriter;

public class Test2 extends HttpServlet {

    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        response.setContentType("text/plain");
        response.setStatus(404);
        PrintWriter writer = response.getWriter();
<<<<<<< HEAD
        writer.print("Buddy Works with Heroku added by kumar Shah new added changes...");
=======
        writer.print("Buddy Works with Heroku added by kumar manjhi from talentica");
>>>>>>> 9d484d9b40ca2a1016d0e1729c91b073e026a9d0
        writer.close();
    }
}
